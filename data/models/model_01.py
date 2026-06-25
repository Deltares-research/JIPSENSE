#!/usr/bin/env python
"""
Model 01: 3-Layer Flat Mesh Generation
This is modified for a 3 layers case, following the description by SPECFEM example
"""

# Import required libraries
import pygmsh
import numpy as np
from meshio2spec2d import *

# Configuration
use_cpml = True

# Initialize empty geometry using the built-in kernel in GMSH
with pygmsh.geo.Geometry() as model:

    # Define global parameters
    H = 3.0  # domain height in meter
    L = 30.0  # domain width in meter

    # H_w = 2.5  # water depth in meter
    # H_g = (H - H_w)  # subsurface depth in meter
    H_layer1 = 0.50  # layer1 depth in meter
    H_layer2 = 0.25  # layer2 depth in meter

    H_w = H - (H_layer1 + H_layer2)  # water depth in meter

    # Element size for both water and subsurface domain
    # lc_w = 0.09375 * 1000
    # lc_g = 0.075 * 1000

    # Test size
    lc_w = 0.15
    lc_g = 0.15

    if use_cpml:
        # PML layer thickness
        n_elm_pml = 6
        pml = lc_g * n_elm_pml

    top_pml = False

    """ node ids without pml layer
    
    
    8             7
    
    5             6 <--- sub-surface topo

    4             3 


    1             2

    """

    """ node ids with pml layer

    19  18            17  16 <--- top_pml = True

    20   O            O   15
                w
    21   O            O   14

              layer1

    22   O            0   13

              layer2

    23   O            O    12

    24   9            10   11
    """

    # All points within the domain. No PML layer
    p1 = model.add_point((0, 0, 0), lc_g)
    p2 = model.add_point((L, 0, 0), lc_g)

    p3 = model.add_point((L, H_layer1, 0), lc_g)
    p4 = model.add_point((0, H_layer1, 0), lc_g)

    p5 = model.add_point((0, H_layer1 + H_layer2, 0), lc_g)
    p6 = model.add_point((L, H_layer1 + H_layer2, 0), lc_g)

    p7 = model.add_point((L, H, 0), lc_w)
    p8 = model.add_point((0, H, 0), lc_w)

    # Points for pml layer outside the domain
    if use_cpml:
        p9 = model.add_point((0, -pml, 0), lc_g)
        p10 = model.add_point((L, -pml, 0), lc_g)
        p11 = model.add_point((L + pml, -pml, 0), lc_g)
        p12 = model.add_point((L + pml, 0, 0), lc_g)

        p13 = model.add_point((L + pml, H_layer1, 0), lc_g)
        p14 = model.add_point((L + pml, H_layer1 + H_layer2, 0), lc_w)
        p15 = model.add_point((L + pml, H, 0), lc_w)

        if top_pml:
            p16 = model.add_point((L + pml, H + pml, 0), lc_w)
            p17 = model.add_point((L, H + pml, 0), lc_w)
            p18 = model.add_point((0, H + pml, 0), lc_w)
            p19 = model.add_point((-pml, H + pml, 0), lc_w)

        p20 = model.add_point((-pml, H, 0), lc_g)
        p21 = model.add_point((-pml, H_layer1 + H_layer2, 0), lc_g)
        p22 = model.add_point((-pml, H_layer1, 0), lc_g)
        p23 = model.add_point((-pml, 0, 0), lc_g)
        p24 = model.add_point((-pml, -pml, 0), lc_g)

    # --------------------Assembling lines--------------------------------

    # Bottom line
    l_bot = model.add_line(p1, p2)
    l_right_layer1 = model.add_line(p2, p3)
    l_right_layer2 = model.add_line(p3, p6)

    # Water/sediment interface
    l_bound_wg = model.add_line(p5, p6)

    # layer1/layer2 interface
    l_bound_layer = model.add_line(p3, p4)

    # Left layer
    l_left_layer1 = model.add_line(p4, p1)
    l_left_layer2 = model.add_line(p5, p4)

    # Top of water
    l_top = model.add_line(p7, p8)

    # Left and right boundaries of water
    l_right_w = model.add_line(p6, p7)
    l_left_w = model.add_line(p5, p8)

    # -----------------------creating line loop-------------------------------
    ll_layer1 = model.add_curve_loop([l_bot, l_right_layer1, l_bound_layer, l_left_layer1])
    ll_layer2 = model.add_curve_loop([-l_bound_layer, l_right_layer2, -l_bound_wg, l_left_layer2])
    ll_w = model.add_curve_loop([l_bound_wg, l_right_w, l_top, -l_left_w])

    # ------------------------plane surface--------------------------------
    ps_layer1 = model.add_plane_surface(ll_layer1)
    ps_layer2 = model.add_plane_surface(ll_layer2)
    ps_w = model.add_plane_surface(ll_w)

    # #################################-----------PML layers------------#################################
    if use_cpml:
        # lines

        # Bottom and left bottom lines
        l_bot_pml = model.add_line(p9, p10)
        l_br_h_pml = model.add_line(p10, p11)
        l_br_v_pml = model.add_line(p11, p12)

        l_br_h2_pml = model.add_line(p2, p12)
        l_br_v2_pml = model.add_line(p2, p10)

        # Left and right lines
        l_r_layer1_pml = model.add_line(p12, p13)
        l_r_layer2_pml = model.add_line(p13, p14)
        l_r_layer2_layer1_pml = model.add_line(p3, p13)
        l_r_gw_pml = model.add_line(p6, p14)
        l_r_w_pml = model.add_line(p14, p15)

        # Top PML lines

        if top_pml:
            l_tr_v_pml = model.add_line(p15, p16)
            l_tr_h_pml = model.add_line(p16, p17)
            l_top_pml = model.add_line(p17, p18)
            l_tl_h_pml = model.add_line(p18, p19)
            l_tl_v_pml = model.add_line(p19, p20)
            l_tr_v2_pml = model.add_line(p7, p17)
            l_tl_v2_pml = model.add_line(p8, p18)

        l_tr_h2_pml = model.add_line(p7, p15)
        l_tl_h2_pml = model.add_line(p8, p20)
        l_l_w_pml = model.add_line(p20, p21)
        l_l_gw_pml = model.add_line(p5, p21)

        l_l_layer1_pml = model.add_line(p22, p23)
        l_l_layer2_pml = model.add_line(p21, p22)
        l_l_layer2_layer1_pml = model.add_line(p4, p22)

        l_bl_v_pml = model.add_line(p23, p24)
        l_bl_h_pml = model.add_line(p24, p9)

        l_bl_v2_pml = model.add_line(p1, p9)
        l_bl_h2_pml = model.add_line(p1, p23)

        # -------------------create curve loops --------------------------------------
        ll_bot_pml = model.add_curve_loop([l_bot_pml, -l_br_v2_pml, -l_bot, l_bl_v2_pml])

        ll_br_pml = model.add_curve_loop([l_br_h_pml, l_br_v_pml, -l_br_h2_pml, l_br_v2_pml])

        ll_r_layer1_pml = model.add_curve_loop([l_br_h2_pml, l_r_layer1_pml, -l_r_layer2_layer1_pml, -l_right_layer1])
        ll_r_layer2_pml = model.add_curve_loop([l_r_layer2_layer1_pml, l_r_layer2_pml, -l_r_gw_pml, -l_right_layer2])
        ll_r_w_pml = model.add_curve_loop([l_r_gw_pml, l_r_w_pml, -l_tr_h2_pml, -l_right_w])

        if top_pml:
            ll_tr_pml = model.add_curve_loop([l_tr_h2_pml, l_tr_v_pml, l_tr_h_pml, -l_tr_v2_pml])
            ll_top_pml = model.add_curve_loop([-l_top, l_tr_v2_pml, l_top_pml, -l_tl_v2_pml])
            ll_tl_pml = model.add_curve_loop([l_tl_v_pml, -l_tl_h2_pml, l_tl_v2_pml, l_tl_h_pml])

        ll_l_w_pml = model.add_curve_loop([l_tl_h2_pml, l_l_w_pml, -l_l_gw_pml, l_left_w])

        ll_l_layer1_pml = model.add_curve_loop([l_l_layer1_pml, -l_bl_h2_pml, -l_left_layer1, l_l_layer2_layer1_pml])

        ll_l_layer2_pml = model.add_curve_loop([-l_l_layer2_layer1_pml, -l_left_layer2, l_l_gw_pml, l_l_layer2_pml])

        ll_bl_pml = model.add_curve_loop([l_bl_h2_pml, l_bl_v_pml, l_bl_h_pml, -l_bl_v2_pml])

        # plane surface
        ps_bot_pml = model.add_plane_surface(ll_bot_pml)
        ps_br_pml = model.add_plane_surface(ll_br_pml)  # plane 4
        ps_r_layer1_pml = model.add_plane_surface(ll_r_layer1_pml)
        ps_r_layer2_pml = model.add_plane_surface(ll_r_layer2_pml)
        ps_r_w_pml = model.add_plane_surface(ll_r_w_pml)  # plane 6

        if top_pml:
            ps_tr_pml = model.add_plane_surface(ll_tr_pml)
            ps_top_pml = model.add_plane_surface(ll_top_pml)
            ps_tl_pml = model.add_plane_surface(ll_tl_pml)

        ps_l_w_pml = model.add_plane_surface(ll_l_w_pml)
        ps_l_layer1_pml = model.add_plane_surface(ll_l_layer1_pml)
        ps_l_layer2_pml = model.add_plane_surface(ll_l_layer2_pml)

        ps_bl_pml = model.add_plane_surface(ll_bl_pml)

    # make cpml layer to be transfinite
    if use_cpml:
        if top_pml:
            model.set_transfinite_curve(l_tl_h_pml, n_elm_pml + 1, "Progression", 1.0)
            model.set_transfinite_curve(l_tr_h_pml, n_elm_pml + 1, "Progression", 1.0)
            model.set_transfinite_curve(l_tl_v_pml, n_elm_pml + 1, "Progression", 1.0)
            model.set_transfinite_curve(l_tr_v_pml, n_elm_pml + 1, "Progression", 1.0)
            model.set_transfinite_curve(l_tl_v2_pml, n_elm_pml + 1, "Progression", 1.0)
            model.set_transfinite_curve(l_tr_v2_pml, n_elm_pml + 1, "Progression", 1.0)

        model.set_transfinite_curve(l_tl_h2_pml, n_elm_pml + 1, "Progression", 1.0)
        model.set_transfinite_curve(l_tr_h2_pml, n_elm_pml + 1, "Progression", 1.0)
        model.set_transfinite_curve(l_l_gw_pml, n_elm_pml + 1, "Progression", 1.0)
        model.set_transfinite_curve(l_r_gw_pml, n_elm_pml + 1, "Progression", 1.0)
        model.set_transfinite_curve(l_bl_h_pml, n_elm_pml + 1, "Progression", 1.0)
        model.set_transfinite_curve(l_br_h_pml, n_elm_pml + 1, "Progression", 1.0)
        model.set_transfinite_curve(l_bl_v_pml, n_elm_pml + 1, "Progression", 1.0)
        model.set_transfinite_curve(l_br_v_pml, n_elm_pml + 1, "Progression", 1.0)
        model.set_transfinite_curve(l_bl_h2_pml, n_elm_pml + 1, "Progression", 1.0)
        model.set_transfinite_curve(l_br_h2_pml, n_elm_pml + 1, "Progression", 1.0)
        model.set_transfinite_curve(l_bl_v2_pml, n_elm_pml + 1, "Progression", 1.0)
        model.set_transfinite_curve(l_br_v2_pml, n_elm_pml + 1, "Progression", 1.0)

        model.set_transfinite_surface(ps_bot_pml, "Left", corner_pts=[p1, p9, p10, p2])
        model.set_transfinite_surface(ps_br_pml, "Left", corner_pts=[p2, p10, p11, p12])
        model.set_transfinite_surface(ps_r_layer1_pml, "Left", corner_pts=[p3, p2, p12, p13])
        model.set_transfinite_surface(ps_r_layer2_pml, "Left", corner_pts=[p6, p3, p13, p14])
        model.set_transfinite_surface(ps_r_w_pml, "Left", corner_pts=[p7, p6, p14, p15])
        model.set_transfinite_surface(ps_l_w_pml, "Left", corner_pts=[p20, p21, p5, p8])
        model.set_transfinite_surface(ps_l_layer1_pml, "Left", corner_pts=[p22, p23, p1, p4])
        model.set_transfinite_surface(ps_l_layer2_pml, "Left", corner_pts=[p21, p22, p4, p5])
        model.set_transfinite_surface(ps_bl_pml, "Left", corner_pts=[p1, p23, p24, p9])

    # recombine surfaces
    if use_cpml:
        if top_pml:
            model.set_recombined_surfaces([ps_layer1, ps_layer2, ps_w,
                                           ps_bot_pml, ps_br_pml, ps_r_layer1_pml, ps_r_layer2_pml, ps_r_w_pml,
                                           ps_tr_pml, ps_top_pml, ps_tl_pml, ps_l_w_pml,
                                           ps_l_layer1_pml, ps_l_layer2_pml, ps_bl_pml])
        else:
            model.set_recombined_surfaces([ps_layer1, ps_layer2, ps_w,
                                           ps_bot_pml, ps_br_pml, ps_r_layer1_pml, ps_r_layer2_pml, ps_r_w_pml,
                                           ps_l_w_pml, ps_l_layer1_pml, ps_l_layer2_pml, ps_bl_pml])

    else:
        model.set_recombined_surfaces([ps_layer1, ps_layer2, ps_w])

    # synchronize
    model.synchronize()

    # physical groups
    # boundary
    if not use_cpml:
        pg_top = model.add_physical(l_top, label="Top")
        pg_bot = model.add_physical(l_bot, label="Bottom")
        pg_left = model.add_physical([l_left_layer1, l_left_layer2, l_left_w], label="Left")
        pg_right = model.add_physical([l_right_layer1, l_right_layer2, l_right_w], label="Right")
    else:
        if top_pml:
            g_top = model.add_physical([l_top_pml, l_tr_h_pml, l_tl_h_pml], label="Top")
            pg_left = model.add_physical([l_tl_v_pml, l_l_w_pml, l_l_layer1_pml, l_l_layer2_pml, l_bl_v_pml], label="Left")
            pg_right = model.add_physical([l_br_v_pml, l_r_layer1_pml, l_r_layer2_pml, l_r_w_pml, l_tr_v_pml], label="Right")

        else:
            pg_top = model.add_physical([l_top, l_tr_h2_pml, l_tl_h2_pml], label="Top")
            pg_left = model.add_physical([l_l_w_pml, l_l_layer1_pml, l_l_layer2_pml, l_bl_v_pml], label="Left")
            pg_right = model.add_physical([l_br_v_pml, l_r_layer1_pml, l_r_layer2_pml, l_r_w_pml], label="Right")

        pg_bot = model.add_physical([l_bot_pml, l_br_h_pml, l_bl_h_pml], label="Bottom")

        # use _* for preparing damping region between PML and main domain
        _pg_top = model.add_physical(l_top, label="_Top")
        _pg_bot = model.add_physical(l_bot, label="_Bottom")
        _pg_left = model.add_physical([l_left_layer1, l_left_layer2, l_left_w], label="_Left")
        _pg_right = model.add_physical([l_right_layer1, l_right_layer2, l_right_w], label="_Right")

    # material
    if not use_cpml:
        pg_layer1 = model.add_physical(ps_layer1, label="M1")  # subsurface
        pg_layer2 = model.add_physical(ps_layer2, label="M2")  # subsurface
        pg_w = model.add_physical(ps_w, label="M3")  # water
    else:

        pg_layer1 = model.add_physical([ps_layer1, ps_bot_pml, ps_bl_pml, ps_br_pml, ps_l_layer1_pml, ps_r_layer1_pml], label="M1")

        pg_layer2 = model.add_physical([ps_layer2, ps_l_layer2_pml, ps_r_layer2_pml], label="M2")

        if top_pml:
            pg_w = model.add_physical([ps_w, ps_top_pml, ps_tl_pml, ps_tr_pml, ps_l_w_pml, ps_r_w_pml], label="M3")
        else:
            pg_w = model.add_physical([ps_w, ps_l_w_pml, ps_r_w_pml], label="M3")

        pg_pml_x = model.add_physical([ps_r_layer1_pml, ps_r_layer2_pml, ps_l_layer1_pml, ps_l_layer2_pml, ps_l_w_pml, ps_r_w_pml], label="PML_X")  # PML in x direction

        if top_pml:
            pg_pml_y = model.add_physical([ps_bot_pml, ps_top_pml], label="PML_Y")
            pg_pml_xy = model.add_physical([ps_br_pml, ps_tl_pml, ps_tr_pml, ps_bl_pml], label="PML_XY")
        else:
            pg_pml_y = model.add_physical([ps_bot_pml], label="PML_Y")
            pg_pml_xy = model.add_physical([ps_br_pml, ps_bl_pml], label="PML_XY")

    # Generate mesh (meshio object)
    # mesh algorithm can be specified by an integer here.
    # details: https://gitlab.onelab.info/gmsh/gmsh/-/blob/master/src/common/GmshDefines.h#L238
    mesh = model.generate_mesh(dim=2, order=2, verbose=True, algorithm=6)

# Write mesh files
mesh.write("mesh.xdmf", file_format='xdmf')
mesh.write("mesh.msh", file_format='gmsh22')

# Convert to SPECFEM2D format
mio2spec = Meshio2Specfem2D(mesh)
mio2spec.write("model_01")

# Write material velocity file
"""
Format:
#(1)domain_id #(2)material_id #(3)rho #(4)vp #(5)vs #(6)Q_k #(7)Q_mu #(8)ani
#
#  where
#     domain_id          : 1=acoustic / 2=elastic / 3=poroelastic
#     material_id        : POSITIVE integer identifier of material block
#     rho                : density
#     vp                 : P-velocity
#     vs                 : S-velocity
#     Q_k                : 9999 = no Q_kappa attenuation
#     Q_mu               : 9999 = no Q_mu attenuation
#     ani                : 0=no anisotropy/ 1,2,.. check with aniso_model.f90
#
# example:
# 2   1 2300 2800 1500 9999.0 9999.0 0
#
# or
#
#(1)domain_id #(2)material_id  tomography elastic  #(3)filename #(4)positive
#
#  where
#     domain_id : 1=acoustic / 2=elastic / 3=poroelastic
#     material_id        : NEGATIVE integer identifier of material block
#     filename           : filename of the tomography file
#     positive           : a positive unique identifier
#
# example:
# 2  -1 tomography elastic tomo.xyz 1
"""

fname = "/home/obandohe/JIPSENSE/JIPSENSE/src/simulation/MESH/nummaterial_velocity_file"

# M1: subsurface
M1_params = "2 1 1850.d0 1900.d0 300.d0 9999 9999 0"

# M2: layer2
M2_params = "2 2 1700.d0 1500.d0 180.d0 9999 9999 0"

# M3: water
M3_params = "1 3 1000.d0 1500.d0 0.d0 9999 9999 0"

with open(fname, "w") as f:
    f.write(M1_params + "\n")
    f.write(M2_params + "\n")
    f.write(M3_params + "\n")

print("Model 01 generation completed successfully!")
print(f"Material velocity file written to: {fname}")
