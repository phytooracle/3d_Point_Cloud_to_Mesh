#!/usr/bin/env python3

import argparse
import open3d as o3d
import pandas as pd
import meshio
import numpy as np
import pyvista as pv
import os

#----------------------------------

def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Individual plant temperature extraction',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-p',
                        '--path',
                        metavar='path',
                        help='Path to the individual point cloud (in .ply format)')

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory where final mesh will be saved',
                        metavar='str',
                        type=str,
                        default='mesh_out')

    return parser.parse_args()

#----------------------------------

def points_to_mesh(cloud):
    
    ## Import point cloud
    pcd = meshio.read(f'{cloud}/combined_multiway_registered.ply')
    
    ## Grabs all of the points that make up the point cloud and cretes a df from the array
    points = pcd.points
    points_df = pd.DataFrame(points, columns=['x', 'y', 'z'])
    
    ## Performs a transformation of each point to scale it
    points_df['x'] = points_df['x'] - 409000
    points_df['y'] = points_df['y'] - 3660100
    points_df['z'] = points_df['z'] - 0.00
    
    ## Converts the new df to an array
    new_points = pd.DataFrame(points_df).to_numpy()
    
    ## Creates PolyData, 3D represtnation and a final mesh
    poly = pv.PolyData(points)
    shell = poly.delaunay_3d(alpha=0.02, progress_bar=True)
    shell_geo = shell.extract_geometry().triangulate()
    
    return (shell_geo)

#----------------------------------

def main():
    args = get_args()
    outdir = args.outdir

    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    cloud = args.path

    final_mesh = points_to_mesh(cloud)

    final_mesh.save(os.path.join(args.outdir, f'{args.path}_mesh.ply'))
    print(f'Done, see outputs in ./{args.outdir}.')

#----------------------------------
if __name__ == '__main__':
    main()