from __future__ import print_function
import numpy as np
import cv2
import subprocess

# PLY header template
ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

# Function to write point cloud data to a PLY file
def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'wb') as f:
        f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
        np.savetxt(f, verts, fmt='%f %f %f %d %d %d')

if __name__ == '__main__':
    print('loading images...')
    imgL = cv2.pyrDown(cv2.imread('images/1.png'))
    imgR = cv2.pyrDown(cv2.imread('images/2.png'))

    # disparity range
    window_size = 3
    min_disp = 2
    num_disp = 20 - min_disp
    stereo = cv2.StereoSGBM_create(minDisparity=min_disp,
                                   numDisparities=num_disp,
                                   blockSize=2,
                                   P1=8 * 3 * window_size ** 2,
                                   P2=32 * 3 * window_size ** 2,
                                   disp12MaxDiff=100,
                                   uniquenessRatio=0,
                                   speckleWindowSize=100,
                                   speckleRange=60
                                   )

    print('computing disparity...')
    disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0

    print('generating 3d point cloud...')
    h, w = imgL.shape[:2]
    f = 0.8 * w
    Q = np.float32([[1, 0, 0, -0.5 * w],
                    [0, -1, 0, 0.5 * h],
                    [0, 0, 0, -f],
                    [0, 0, 1, 0]])
    points = cv2.reprojectImageTo3D(disp, Q)
    colors = cv2.cvtColor(imgL, cv2.COLOR_BGR2RGB)
    mask = disp > disp.min()
    out_points = points[mask]
    out_colors = colors[mask]
    out_fn = 'out.ply'
    write_ply(out_fn, out_points, out_colors)
    print(f'{out_fn} saved')
    subprocess.run(["open", out_fn])

    cv2.imshow('left', imgL)
    cv2.imshow('disparity', (disp - min_disp) / num_disp)

    cv2.waitKey()
    cv2.destroyAllWindows()
