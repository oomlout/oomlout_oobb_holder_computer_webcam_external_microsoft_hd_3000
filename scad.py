import copy
import opsc
import oobb
import oobb_base

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    # save_type variables
    if True:
        filter = ""
        #filter = "base"

        #kwargs["save_type"] = "none"
        kwargs["save_type"] = "all"
        
        kwargs["overwrite"] = True
        
        #kwargs["modes"] = ["3dpr", "laser", "true"]
        kwargs["modes"] = ["3dpr"]
        #kwargs["modes"] = ["laser"]

    # default variables
    if True:
        kwargs["size"] = "oobb"
        kwargs["width"] = 5
        kwargs["height"] = 3
        kwargs["thickness"] = 3

    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        part_default = {} 
        part_default["project_name"] = "oobb_holder_computer_webcam_external_microsoft_hd_3000" ####### neeeds setting
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        
        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        #p3["thickness"] = 6
        part["kwargs"] = p3
        part["name"] = "base"
        parts.append(part)

        part = copy.deepcopy(part_default)
        p3 = copy.deepcopy(kwargs)
        p3["thickness"] = 13
        p3["width"] = 3
        part["kwargs"] = p3
        part["name"] = "cover"
        parts.append(part)

        
    #make the parts
    if True:
        for part in parts:
            name = part.get("name", "default")
            if filter in name:
                print(f"making {part['name']}")
                make_scad_generic(part)            
                print(f"done {part['name']}")
            else:
                print(f"skipping {part['name']}")

def get_base(thing, **kwargs):

    depth = kwargs.get("thickness", 4)
    prepare_print = kwargs.get("prepare_print", False)

    pos = kwargs.get("pos", [0, 0, 0])
    #pos = copy.deepcopy(pos)
    #pos[2] += -20

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"    
    p3["both_holes"] = True
    p3["depth"] = depth
    p3["holes"] = ["left","right","top"]
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #extra holes
    #add holes zip tie
    #add zip tie clearance square
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_zip_tie_clearance_small"
    pos1 = copy.deepcopy(pos1)
    pos1[0] += 2*15
    p3["pos"] = pos1
    #p3["m"] = "#"
    oobb_base.append_full(thing,**p3)

    

    import yaml
    with open('oobb_data/mounting_holes.yaml', 'r') as file:
        mounting_holes = yaml.load(file, Loader=yaml.FullLoader)

    
    #add holes
    for position_hole in mounting_holes:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_hole"
        p3["pos"] = position_hole["pos"]
        p3["radius_name"] = position_hole["radius_name"]
        #p3["m"] = "#" 
        oobb_base.append_full(thing,**p3)   
        
        #add cylinder for screw
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "p"
        p3["shape"] = f"oobb_cylinder"
        lift = 3 + 5 # add three as it is from the base
        p3["depth"] = lift #full length of screw
        pos1 = copy.deepcopy(position_hole["pos"])
        pos1[2] += lift/2
        p3["pos"] = pos1
        p3["radius"] = 3/2
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)
        
        #add cylinder for support
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "p"
        p3["shape"] = f"oobb_cylinder"
        lift = lift-1.5
        p3["depth"] = lift #full length of screw
        pos1 = copy.deepcopy(position_hole["pos"])
        pos1[2] += lift/2
        p3["pos"] = pos1
        p3["radius"] = 6/2
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

    kwargs["lift_screw"] = 3
    get_connecting_screws(thing, **kwargs)



def get_cover(thing, **kwargs):

    depth = kwargs.get("thickness", 4)
    prepare_print = kwargs.get("prepare_print", False)

    pos = kwargs.get("pos", [0, 0, 0])
    #pos = copy.deepcopy(pos)
    #pos[2] += -20



    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    #add holes
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"    
    p3["both_holes"] = True
    p3["depth"] = depth
    p3["holes"] = "perimeter"
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add cavity cube
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cube"
    p3["size"] = [37,25,depth-2]
    pos1 = copy.deepcopy(pos)
    pos1[2] += 0
    p3["pos"] = pos1
    #p3["m"] = "#"
    oobb_base.append_full(thing,**p3)

    # add cable escape cube
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cube"
    p3["size"] = [8,8,5]
    pos1 = copy.deepcopy(pos)
    pos1[0] += 20
    pos1[1] += 0
    pos1[2] += 0
    p3["pos"] = pos1
    #p3["m"] = "#"
    oobb_base.append_full(thing,**p3)


    #lens hole
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_hole"
    pos1 = copy.deepcopy(pos)
    pos1[2] += 0
    p3["pos"] = pos1
    p3["radius"] = 10/2
    #p3["m"] = "#"
    oobb_base.append_full(thing,**p3)

    get_connecting_screws(thing, **kwargs)

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)


def get_connecting_screws(thing, **kwargs):    
    pos = kwargs.get("pos", [0, 0, 0])
    lift_screw = kwargs.get("lift_screw", 0)

    position_screws = []
    dep = kwargs.get("thickness", None) 
    position_screws.append([7.5,15,dep])
    position_screws.append([7.5,-15,dep])
    position_screws.append([-7.5,15,dep])
    position_screws.append([-7.5,-15,dep])

    for position_screw in position_screws:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_screw_countersunk"  
        p3["depth"] = dep + 3   
        p3["radius_name"] = "m3"
        pos1 = copy.deepcopy(position_screw)
        pos1[2] += lift_screw
        p3["pos"] = pos1
        p3["nut"] = True
        p3["m"] = "#"
        oobb_base.append_full(thing,**p3)





    

    

    
    
###### utilities



def make_scad_generic(part):
    
    # fetching variables
    name = part.get("name", "default")
    project_name = part.get("project_name", "default")
    
    kwargs = part.get("kwargs", {})    
    
    modes = kwargs.get("modes", ["3dpr", "laser", "true"])
    save_type = kwargs.get("save_type", "all")
    overwrite = kwargs.get("overwrite", True)

    kwargs["type"] = f"{project_name}_{name}"

    thing = oobb_base.get_default_thing(**kwargs)
    kwargs.pop("size","")

    #get the part from the function get_{name}"
    func = globals()[f"get_{name}"]
    func(thing, **kwargs)

    for mode in modes:
        depth = thing.get(
            "depth_mm", thing.get("thickness_mm", 3))
        height = thing.get("height_mm", 100)
        layers = depth / 3
        tilediff = height + 10
        start = 1.5
        if layers != 1:
            start = 1.5 - (layers / 2)*3
        if "bunting" in thing:
            start = 0.5
        opsc.opsc_make_object(f'scad_output/{thing["id"]}/{mode}.scad', thing["components"], mode=mode, save_type=save_type, overwrite=overwrite, layers=layers, tilediff=tilediff, start=start)    


if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)