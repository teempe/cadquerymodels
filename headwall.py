import cadquery as cq


# base slab width varies from 1560mm to 685mm length 1220mm
# base thickness 100mm
# back wall height 1000mm with opening 400mm dia.
# wingwalls height varies from 1000mm to 320mm
# walls thickness 100mm
# shear key depth 600mm


# base slab (with walls thickness)
base_pts = [(0.0, 0.0), (1560.0, 0.0), (1654.13, 33.76), (1192.87, 1320.0),
            (367.13, 1320.0), (-94.13, 33.76), (0.0, 0.0)]

headwall = cq.Workplane("XY") \
                .polyline(base_pts).close() \
                .extrude(-100)

# back wall
backw_pts = [(331.26, 1220.0), (1228.73, 1220.0), (1192.87, 1320.0), 
             (367.13, 1320.0), (331.26, 1220.0)]

headwall = headwall \
                .polyline(backw_pts).close() \
                .extrude(1000)

# opening
open_dia = 400.0
open_centre = (780.0, 1220.0, open_dia/2 + 100.0)

headwall = headwall \
                .copyWorkplane(cq.Workplane("XZ", origin=open_centre)) \
                .circle(open_dia/2) \
                .cutThruAll()

# wing walls
wingw_front_pts = [(0.0, 0.0), (-100.0, 0.0), (-100.0, 320.0), (0.0, 320.0), (0.0, 0.0)]
wingw_back_pts = [(0.0, 0.0), (-106.24, 0.0), (-106.24, 1000.0), (0.0, 1000.0), (0.0, 0.0)]

#left wing wall
headwall = headwall \
                .copyWorkplane(cq.Workplane("XZ")) \
                .transformed(rotate=cq.Vector(0,-20, 0)) \
                .polyline(wingw_front_pts).close() \
                .copyWorkplane(cq.Workplane("XZ", origin=(437.5, 1220.0))) \
                .polyline(wingw_back_pts).close() \
                .loft(combine=True)

# right wing wall
headwall = headwall \
                .copyWorkplane(cq.Workplane("XZ", origin=(1654.13, 33.76, 0))) \
                .transformed(rotate=cq.Vector(0, 20, 0)) \
                .polyline(wingw_front_pts).close() \
                .copyWorkplane(cq.Workplane("XZ", origin=(1228.73, 1220.0))) \
                .polyline(wingw_back_pts).close() \
                .loft(combine=True)

# shear key
shear_top_pts = [(0.0, 0.0), (-94.13, 33.76), (-34.51, 200.0), 
                 (1594.51, 200.0), (1654.13, 33.76), (1560.0 ,0.0), (0.0, 0.0)]

shear_bot_pts = [(0.0, 0.0), (-94.13, 33.76), (-70.37, 100.0), (1630.37, 100.0), 
                 (1654.13, 33.76), (1560.0 ,0.0), (0.0, 0.0)]

headwall = headwall \
                .copyWorkplane(cq.Workplane("XY", origin=(0, 0, -100))) \
                .polyline(shear_top_pts).close() \
                .copyWorkplane(cq.Workplane("XY", origin=(0, 0, -700))) \
                .polyline(shear_bot_pts).close().loft()

show_object(headwall, options={"color":(192, 192, 192)})