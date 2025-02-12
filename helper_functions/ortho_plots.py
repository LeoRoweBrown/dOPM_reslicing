import tifffile as tiff
import numpy as np
import matplotlib.pyplot as plt

def load_multipage_tiff(filename):
    """Load a multipage TIFF file as a 3D NumPy array."""
    return tiff.imread(filename)

def compute_projections(image_stack):
    """Compute maximum intensity projections along three orthogonal axes."""
    mip_xy = np.max(image_stack, axis=0)  # Top-down view
    mip_xz = np.max(image_stack, axis=1)  # Front view
    mip_yz = np.max(image_stack, axis=2)  # Side view
    return mip_xy, mip_xz, mip_yz

def plot_projections(mip_xy, mip_xz, mip_yz):
    """Arrange and display the projections in a single figure."""
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    axes[0, 0].imshow(mip_xy, cmap="gray")
    axes[0, 0].set_title("Top-down (XY)")

    axes[1, 0].imshow(mip_xz, cmap="gray")
    axes[1, 0].set_title("Front (XZ)")

    axes[0, 1].imshow(mip_yz.T, cmap="gray")  # Transposed for proper orientation
    axes[0, 1].set_title("Side (YZ)")

    axes[1, 1].axis("off")  # Empty subplot for layout balance

    plt.tight_layout()
    plt.show()
    return fig

def plot_gray_orthomips(filename):
    """Load a multipage TIFF, compute orthogonal MIPs, and display them."""

    # Processing
    image_stack = load_multipage_tiff(filename)
    mip_xy, mip_xz, mip_yz = compute_projections(image_stack)
    fig = plot_projections(mip_xy, mip_xz, mip_yz)
    return fig

# Example usage:
# process_tiff_and_plot("path-to-tiff/your_multipage_tiff.tif")


#### now like the legacy MATLAB one

def create_orthomips(filename):

    def load_multipage_tiff_hyperstack(filename):
        """
        Load a multipage TIFF file as a 3D NumPy array.
        for some reason hyperstacks are saved as zcyx(t) in imageJ.
        Format them more sensibly as czyx
        """
        stack_zcyx = tiff.imread(filename)
        print("shape as read", stack_zcyx.shape)
        stack_czyx = np.transpose(stack_zcyx, (1, 0, 3, 2))  # Moves Channels to last dimension
        print(stack_czyx.shape)
        return stack_czyx

    def arrange_mips(stack_zyx, pad_px=20):

        # (transpose so y is horizontal)
        mip_xy = np.max(stack_zyx, axis=0).T  # Top-down view
        mip_xz = np.max(stack_zyx, axis=1).T  # Front view
        mip_yz = np.max(stack_zyx, axis=2)  # Side view

        xdim = stack_zyx.shape[2]
        ydim = stack_zyx.shape[1]
        zdim = stack_zyx.shape[0]

        print("xdim", xdim, "ydim", ydim, "zdim", zdim)
        print("mip_xy.shape", mip_xy.shape, "mip_xz.shape", mip_xz.shape, "mip_yz.shape", mip_yz.shape)

        height = xdim + pad_px + zdim
        width = ydim + pad_px + zdim

        mip_montage = np.zeros((height, width))
        mip_montage[0:xdim, 0:ydim] = mip_xy
        mip_montage[xdim+pad_px:height, 0:ydim] = mip_yz
        mip_montage[0:xdim, (ydim+pad_px):width] = mip_xz

        return mip_montage


    hyperstack = load_multipage_tiff_hyperstack(filename)
    mip_montage_channels = []
    for c_i in range(hyperstack.shape[0]):
        mip_xy, mip_xz, mip_yz = compute_projections(hyperstack[:,:,c_i])
        # plot_projections(mip_xy, mip_xz, mip_yz)
        mip_montage = arrange_mips(hyperstack[c_i,:,:,:])
        mip_montage_channels.append(mip_montage)
        fig = plt.figure() #figsize=(10, 10))
        plt.imshow(mip_montage)
        
    mip_mutlichannel = np.asarray(mip_montage_channels, dtype=np.uint16)#.transpose((1,2,0))

    return mip_mutlichannel



