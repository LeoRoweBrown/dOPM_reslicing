import numpy as np

def scale_matrix(sx=1, sy=1, sz=1):
    """
    Generate a 4x4 affine matrix for scaling transformation.
    
    Parameters:
    sx (float): Scaling factor along the x-axis.
    sy (float): Scaling factor along the y-axis.
    sz (float): Scaling factor along the z-axis.
    
    Returns:
    np.ndarray: 4x4 affine matrix for scaling transformation.
    """
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])

def skew_matrix(theta_s):
    """
    Generate a 4x4 affine matrix for skew transformation in yz plane.
    
    Parameters:
    sz (float): Resulting angle of skew transformation in yz plane.
    
    Returns:
    np.ndarray: 4x4 affine matrix for skew transformation.
    """
    return np.array([
        [1, 0, 0, 0],
        [0, 1, theta_s, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def rotation_matrix(theta, axis='z'):
    """
    Generate a 4x4 affine matrix for rotation transformation about the x,
    y or z-axis.
    
    Parameters:
    theta (float): Rotation angle in radians.
    
    Returns:
    np.ndarray: 4x4 affine matrix for rotation transformation.
    """
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    if axis == 'z':
        return np.array([
            [cos_theta, -sin_theta, 0, 0],
            [sin_theta, cos_theta, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
    elif axis == 'y':
        return np.array([
            [cos_theta, 0, sin_theta, 0],
            [0, 1, 0, 0],
            [-sin_theta, 0, cos_theta, 0],
            [0, 0, 0, 1]
        ])
    elif axis == 'x':
        return np.array([
            [1, 0, 0, 0],
            [0, cos_theta, -sin_theta, 0],
            [0, sin_theta, cos_theta, 0],
            [0, 0, 0, 1]
        ])

def translation_matrix(tx, ty, tz=0):
    """
    Generate a 4x4 affine matrix for translation transformation.
    
    Parameters:
    tx (float): Translation along the x-axis.
    ty (float): Translation along the y-axis.
    tz (float): Translation along the z-axis.
    
    Returns:
    np.ndarray: 4x4 affine matrix for translation transformation.
    """
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])