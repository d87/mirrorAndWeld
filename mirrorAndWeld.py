#python

import traceback

def make_matcher(plane):
    if plane == "+z":
        return lambda pos: pos[0] < -0.00000000001  #vert's x < 0
    elif plane == "-z":
        return lambda pos: pos[0] > 0.00000000001
    elif plane == "+y":
        return lambda pos: pos[1] < -0.00000000001  #y < 0
    elif plane == "-y":
        return lambda pos: pos[1] > 0.00000000001
    elif plane == "+x":
        return lambda pos: pos[2] < -0.00000000001  #z < 0
    elif plane == "-x":
        return lambda pos: pos[2] > 0.00000000001

def main(plane=None):
    symmetry_state = lx.eval('select.symmetryState ?')

    if plane == None:
        if symmetry_state == "none":
            plane = "+x"
        else:
            plane = "+"+symmetry_state

    if plane == "+x" or plane == "-x":
        params = ("y", 9999,0,0, make_matcher(plane), 2)
    elif plane == "+y" or plane == "-y":
        params = ("x", 0,0,9999, make_matcher(plane), 1)
    elif plane == "+z" or plane == "-z":
        params = ("y", 0,0,9999, make_matcher(plane), 0)



    lx.eval('select.symmetryState none') # disable symmetry

    # deselect everything
    lx.eval('select.drop vertex')
    lx.eval('select.drop edge')
    lx.eval('select.drop polygon')


    layer = lx.eval('query layerservice layer.index ? main')


    # lx.eval('select.type polygon')

    axis, sx, sy, sz, match, mirror_axis = params

    lx.eval("tool.set poly.knife on")
    lx.eval("tool.setAttr poly.knife infinite true")
    lx.eval("tool.setAttr poly.knife split false")  # if splitting by polygons then this should be on, in vertex mode off
    lx.eval("tool.setAttr poly.knife axis %s" % axis)
    lx.eval("tool.setAttr poly.knife startX %f" % (-sx))
    lx.eval("tool.setAttr poly.knife startY %f" % (-sy))
    lx.eval("tool.setAttr poly.knife startZ %f" % (-sz))
    lx.eval("tool.setAttr poly.knife endX %f" % (sx))
    lx.eval("tool.setAttr poly.knife endY %f" % (sy))
    lx.eval("tool.setAttr poly.knife endZ %f" % (sz))
    lx.eval("tool.apply")
    lx.eval("tool.set poly.knife off")


    verts = lx.eval('query layerservice verts ? all')
    # polys = lx.eval('query layerservice polys ? all')

    lx.eval('select.type vertex')

    for vertIndex in verts:
        pos = lx.eval('query layerservice vert.pos ? %s' % vertIndex )
        # x,y,z = pos
        if match(pos):
            lx.eval('select.element %s vert add %s' % (layer, vertIndex))
            # lx.out(pos)
            

    # for polyIndex in polys:
    #     pos = lx.eval('query layerservice poly.pos ? %s' % polyIndex )
    #     x,y,z = pos
    #     lx.out("data", x,y,z)
    #     if x < 0:
    #         lx.eval('select.element %s polygon add %s' % (layer, polyIndex))

    # lx.eval('select.convert polygon')


    lx.eval('delete')

    lx.eval('tool.set *.mirror on')
    lx.eval('tool.attr gen.mirror axis %d' % mirror_axis) # 0 = x; 1 = y; 2 = z
    lx.eval('tool.attr gen.mirror cenX 0.0')
    lx.eval('tool.apply')
    lx.eval('tool.set *.mirror off')

    lx.eval('select.symmetryState %s' % symmetry_state) # restore symmetry


if __name__ == '__main__':
   try:
      main(*lx.args())
   except:
      lx.out(traceback.format_exc())