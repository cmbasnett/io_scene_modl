import bpy
import bpy_extras
import bmesh
from bpy.props import StringProperty
from .reader import AsciiModelReader
import os


class ImportOperator(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):

    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = 'io_scene_modl.modl_import'  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = 'Import Lithtech MODL'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    # ImportHelper mixin class uses this
    filename_ext = ".model00a"

    filter_glob = StringProperty(
        default="*.model00a",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        model = AsciiModelReader().from_file(self.filepath)
        model.name = os.path.splitext(os.path.basename(self.filepath))[0]
        armature_data = bpy.data.armatures.new(model.name)
        armature_object = bpy.data.objects.new(model.name, armature_data)
        context.scene.objects.link(armature_object)

        ''' Create materials. '''
        materials = []
        for shape_index, shape in enumerate(model.shapes):
            while len(materials) <= shape.material_index:
                ''' Create a material for the new piece. '''
                material = bpy.data.materials.new(shape.name) # TODO: if material indices are out-of-order, the name might be wrong!
                materials.append(material)

                ''' Create texture. '''
                texture = bpy.data.textures.new(shape.name, type='IMAGE')
                # TODO: not sure where we'd get this from (DDS?)

                texture_slot = material.texture_slots.add()
                texture_slot.texture = texture

        print(materials)

        for shape_index, shape in enumerate(model.shapes):
            mesh_data = bpy.data.meshes.new(shape.name)
            mesh_object = bpy.data.objects.new(shape.name, mesh_data)

            bm = bmesh.new()
            bm.from_mesh(mesh_data)

            ''' Add materials to mesh. '''
            for material in materials:
                ''' Create UV map. '''
                uv_texture = mesh_data.uv_textures.new()
                mesh_data.materials.append(material)
                material.texture_slots[0].uv_layer = uv_texture.name

            # Vertices
            for vertex in shape.vertices:
                bm.verts.new(vertex)
            bm.verts.ensure_lookup_table()

            # Faces
            for face_index, face in enumerate(shape.faces):
                face = [bm.verts[x] for x in face]
                try:
                    bmface = bm.faces.new(face)
                except ValueError:
                    '''
                    This face is a duplicate of another face, which is disallowed by Blender.
                    Mark this face for deletion after iteration.
                    '''
                    #duplicate_face_indices.append(face_index)
                    continue
                '''
                Assign the material index of face based on the piece's material index.
                '''
                bmface.material_index = model.shapes[shape_index].material_index
                #bmface.smooth = True

            '''
            Assign texture coordinates.
            '''
            #material_face_offsets = [0] * len(mesh.materials)

            # TODO: we gotta make a new material, if necessary

            '''
            uv_texture = mesh_data.uv_layers[shape.material_index]  # TODO: shape material index???
            for face_index, face in enumerate(shape.faces):
                material_face_offset = material_face_offsets[0]
                texcoords = [vertex.texcoord for vertex in face.vertices]
                for i in range(3):
                    uv = texcoords[i][0], 1.0 - texcoords[i][1]
                    uv_texture.data[(material_face_offset + face_index) * 3 + i].uv = uv
            material_face_offsets[0] += len(lod.faces)
            '''

            bm.faces.ensure_lookup_table()

            bm.to_mesh(mesh_data)

            mesh_data.validate(clean_customdata=False)
            mesh_data.update(calc_edges=False)

            context.scene.objects.link(mesh_object)

            mesh_object.parent = armature_object

        return {'FINISHED'}

    @staticmethod
    def menu_func_import(self, content):
        self.layout.operator(ImportOperator.bl_idname, text='Lithtech MODL (.model00a)')
