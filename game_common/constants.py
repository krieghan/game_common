from OpenGL import GLUT

GL_DIRECTIONS = {
        GLUT.GLUT_KEY_UP : (0, 1),
        GLUT.GLUT_KEY_DOWN : (0, -1),
        GLUT.GLUT_KEY_LEFT : (-1, 0),
        GLUT.GLUT_KEY_RIGHT : (1, 0)}

def get_direction_from_gl_cursor(gl_cursor):
    return GL_DIRECTIONS.get(gl_cursor)




        
