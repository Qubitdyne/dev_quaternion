#include <linux/module.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/random.h>
#include <linux/device.h>
#include <linux/slab.h> // For kmalloc and kfree
#include <linux/string.h> // For snprintf

#define DEVICE_NAME "quaternion"
#define CLASS_NAME "quaternion"
#define MAX_QUATERNIONS 128
#define SCALING_FACTOR 1600 // Fixed-point scaling by 100 (e.g., 1600 == 16.00)

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Nikolas J. Britton");
MODULE_DESCRIPTION("A /dev interface for generating indeterministic quaternion complex numbers");
MODULE_VERSION("1.0");

static int major_number;
static struct class* quaternion_class = NULL;
static struct device* quaternion_device = NULL;

struct quaternion {
    int h; // Fixed-point representation
    int i;
    int j;
    int k;
};

// Generate values for quaternion components based on Euler's formula logic
static int generate_component_fixed(int base, int scaling_factor) {
    unsigned int rand;
    get_random_bytes(&rand, sizeof(rand));
    int value = (base + (rand % (scaling_factor * 2)) - scaling_factor);

    if (value > scaling_factor) {
        value = scaling_factor;
    } else if (value < -scaling_factor) {
        value = -scaling_factor;
    }

    return value;
}

static ssize_t dev_read(struct file* filep, char* buffer, size_t len, loff_t* offset) {
    struct quaternion *quats;
    char *output_buffer;
    size_t quats_to_generate = len / 64; // Each quaternion string is ~64 bytes
    size_t i, total_output_size = 0;
    int ret;

    if (quats_to_generate > MAX_QUATERNIONS) {
        quats_to_generate = MAX_QUATERNIONS;
    }

    // Allocate memory for quaternions and output buffer
    quats = kmalloc(quats_to_generate * sizeof(struct quaternion), GFP_KERNEL);
    if (!quats) {
        printk(KERN_ERR "Failed to allocate memory for quaternions\n");
        return -ENOMEM;
    }

    output_buffer = kmalloc(quats_to_generate * 64, GFP_KERNEL);
    if (!output_buffer) {
        printk(KERN_ERR "Failed to allocate memory for output buffer\n");
        kfree(quats);
        return -ENOMEM;
    }

    // Generate quaternions
    for (i = 0; i < quats_to_generate; i++) {
        quats[i].h = generate_component_fixed(0, SCALING_FACTOR);
        quats[i].i = generate_component_fixed(0, SCALING_FACTOR);
        quats[i].j = generate_component_fixed(0, SCALING_FACTOR);
        quats[i].k = generate_component_fixed(0, SCALING_FACTOR);

        // Convert fixed-point values to string representation
	// Q = ah + bi + cj + dk
        total_output_size += snprintf(output_buffer + total_output_size, 64,
                                      "%d.%02d %d.%02d %d.%02d %d.%02d\n",
                                      quats[i].h / 100, abs(quats[i].h % 100),
                                      quats[i].i / 100, abs(quats[i].i % 100),
                                      quats[i].j / 100, abs(quats[i].j % 100),
                                      quats[i].k / 100, abs(quats[i].k % 100));
    }

    // Copy the formatted string to user space
    ret = copy_to_user(buffer, output_buffer, total_output_size);
    if (ret != 0) {
        printk(KERN_ERR "Failed to copy quaternion data to user\n");
        kfree(quats);
        kfree(output_buffer);
        return -EFAULT;
    }

    kfree(quats);
    kfree(output_buffer);
    return total_output_size;
}

static int dev_open(struct inode* inodep, struct file* filep) {
    printk(KERN_INFO "Quaternion device opened\n");
    return 0;
}

static int dev_release(struct inode* inodep, struct file* filep) {
    printk(KERN_INFO "Quaternion device closed\n");
    return 0;
}

static struct file_operations fops = {
    .open = dev_open,
    .read = dev_read,
    .release = dev_release,
};

static int __init quaternion_init(void) {
    printk(KERN_INFO "Initializing Quaternion device\n");

    major_number = register_chrdev(0, DEVICE_NAME, &fops);
    if (major_number < 0) {
        printk(KERN_ALERT "Failed to register a major number\n");
        return major_number;
    }
    printk(KERN_INFO "Registered device with major number %d\n", major_number);

    quaternion_class = class_create(CLASS_NAME);
    if (IS_ERR(quaternion_class)) {
        unregister_chrdev(major_number, DEVICE_NAME);
        printk(KERN_ALERT "Failed to register device class\n");
        return PTR_ERR(quaternion_class);
    }
    printk(KERN_INFO "Device class registered\n");

    quaternion_device = device_create(quaternion_class, NULL, MKDEV(major_number, 0), NULL, DEVICE_NAME);
    if (IS_ERR(quaternion_device)) {
        class_destroy(quaternion_class);
        unregister_chrdev(major_number, DEVICE_NAME);
        printk(KERN_ALERT "Failed to create the device\n");
        return PTR_ERR(quaternion_device);
    }
    printk(KERN_INFO "Device created successfully\n");

    return 0;
}

static void __exit quaternion_exit(void) {
    device_destroy(quaternion_class, MKDEV(major_number, 0));
    class_unregister(quaternion_class);
    class_destroy(quaternion_class);
    unregister_chrdev(major_number, DEVICE_NAME);
    printk(KERN_INFO "Quaternion device unregistered\n");
}

module_init(quaternion_init);
module_exit(quaternion_exit);
