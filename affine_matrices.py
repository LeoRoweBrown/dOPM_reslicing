import numpy as np

def identity_matrix(square=True):
    """
    Generate a 4x4 or 3x4 affine matrix for identity transformation.
    
    Returns:
    np.ndarray: 4x4 or 3x4 (if square=False) affine matrix for identity transformation.
    """
    matrix = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    if not square:
        matrix = np.delete(matrix, (3), axis=0)
    
    return matrix

def scale_matrix(sx=1, sy=1, sz=1, square=True):
    """
    Generate a 4x4 or 3x4 affine matrix for scaling transformation.
    
    Parameters:
    sx (float): Scaling factor along the x-axis.
    sy (float): Scaling factor along the y-axis.
    sz (float): Scaling factor along the z-axis.
    
    Returns:
    np.ndarray: 4x4 or 3x4 (if square=False) affine matrix for scaling transformation.
    """ 
    matrix = np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])
    if not square:
        matrix = np.delete(matrix, (3), axis=0)

    return matrix

def skew_matrix(theta_s, square=True):
    """
    Generate a 4x4 or 3x4 affine matrix for skew transformation in yz plane.
    
    Parameters:
    sz (float): Resulting angle of skew transformation in yz plane.
    
    Returns:
    np.ndarray: 4x4 or 3x4 (if square=False) affine matrix for skew transformation.
    """
    matrix = np.array([
        [1, 0, 0, 0],
        [0, 1, theta_s, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    if not square:
        matrix = np.delete(matrix, (3), axis=0)

    return matrix

def rotation_matrix(theta, axis='z', square=True):
    """
    Generate a 4x4 or 3x4 affine matrix for rotation transformation about the x,
    y or z-axis.
    
    Parameters:
    theta (float): Rotation angle in radians.
    
    Returns:
    np.ndarray: 4x4 or 3x4 (if square=False) affine matrix for rotation transformation.
    """
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    if axis == 'z':
        matrix = np.array([
            [cos_theta, -sin_theta, 0, 0],
            [sin_theta, cos_theta, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
    elif axis == 'y':
        matrix = np.array([
            [cos_theta, 0, sin_theta, 0],
            [0, 1, 0, 0],
            [-sin_theta, 0, cos_theta, 0],
            [0, 0, 0, 1]
        ])
    else: # axis == 'x'
        matrix = np.array([
            [1, 0, 0, 0],
            [0, cos_theta, -sin_theta, 0],
            [0, sin_theta, cos_theta, 0],
            [0, 0, 0, 1]
        ])
    if not square: 
        matrix = np.delete(matrix, (3), axis=0)

        
    return matrix

def translation_matrix(tx=0, ty=0, tz=0, square=True):
    """
    Generate a 4x4 or 3x4 affine matrix for translation transformation.
    
    Parameters:
    tx (float): Translation along the x-axis.
    ty (float): Translation along the y-axis.
    tz (float): Translation along the z-axis.
    
    Returns:
    np.ndarray: 4x4 or 3x4 (if square=False) affine matrix for translation transformation.
    """
    matrix = np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])
    if not square:
        matrix = np.delete(matrix, (3), axis=0)
    
    return matrix