import pygame
import math
import random
import time
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

pygame.init()
glutInit()

width, height = 1280, 800
pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)

gluPerspective(60, (width / height), 0.1, 100.0)
glTranslatef(0.0, 0.0, -5)
glClearColor(0.1, 0.1, 0.2, 1.0)  # Warna latar belakang hitam
glEnable(GL_DEPTH_TEST)          # Aktifkan depth buffer
glEnable(GL_BLEND)               # Aktifkan transparansi
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Aktifkan pencahayaan
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)

# Perbarui properti pencahayaan
light_position = [1.5, -1.5, -4.0, 1.0]  # Diposisikan di tengah akuarium
light_ambient = [0.4, 0.4, 0.4, 1.0]   # Cahaya ambient lebih terang
light_diffuse = [0.8, 0.8, 0.8, 1.0]   # Cahaya diffuse
light_specular = [1.0, 1.0, 1.0, 1.0]  # Cahaya specular

glLightfv(GL_LIGHT0, GL_POSITION, light_position)
glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

# Aktifkan properti material
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

# Atur cahaya ambient global
global_ambient = [0.1, 0.1, 0.1, 1.0]
glLightModelfv(GL_LIGHT_MODEL_AMBIENT, global_ambient)

angle_x = 0
angle_y = 0
radius = 0.01

def draw_fish(position):
    "Menggambar ikan pertama."
    x, y, z = position

    # Pergerakan ikan
    glPushMatrix()
    glTranslatef(x, y, z)

    # Badan ikan
    glPushMatrix()
    glScalef(1.5, 1.0, 1.0)  
    glColor3f(1, 0.5, 0)  
    quad = gluNewQuadric()
    gluSphere(quad, 0.2, 32, 32)  
    gluDeleteQuadric(quad)
    glPopMatrix()

    # Ekor ikan
    glPushMatrix()
    glTranslatef(-0.3, 0.0, 0.0)  
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(1.0, 0.3, 0.0)  
    glVertex3f(0.0, 0.0, 0.0)  
    glVertex3f(-0.2, 0.15, 0.05)
    glVertex3f(-0.3, 0.1, 0.05)
    glVertex3f(-0.35, 0.0, 0.0)
    glVertex3f(-0.3, -0.1, -0.05)
    glVertex3f(-0.2, -0.15, -0.05)
    glVertex3f(0.0, 0.0, 0.0)  
    glEnd()
    glPopMatrix()

    # Sirip atas
    glPushMatrix()
    glTranslatef(0.0, 0.25, 0.0)  
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(1.0, 0.7, 0.0)  
    glVertex3f(0.0, 0.1, 0.0)  
    glVertex3f(0.05, 0.0, 0.05)
    glVertex3f(0.1, -0.05, 0.0)
    glVertex3f(0.05, -0.1, -0.05)
    glVertex3f(-0.05, -0.1, -0.05)
    glVertex3f(-0.1, -0.05, 0.0)
    glVertex3f(-0.05, 0.0, 0.05)
    glVertex3f(0.0, 0.1, 0.0) 
    glEnd()
    glPopMatrix()

    # Sirip kanan
    glPushMatrix()
    glTranslatef(0.1, 0.0, 0.2)
    glRotatef(45, 1, 0, 0) 
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(1.0, 0.6, 0.0)
    glVertex3f(0.0, 0.0, 0.0) 
    glVertex3f(0.1, 0.05, 0.0)
    glVertex3f(0.15, 0.0, 0.0)
    glVertex3f(0.1, -0.05, 0.0)
    glVertex3f(0.0, -0.1, 0.0)
    glVertex3f(-0.1, -0.05, 0.0)
    glVertex3f(-0.15, 0.0, 0.0)
    glVertex3f(-0.1, 0.05, 0.0)
    glVertex3f(0.0, 0.0, 0.0)  
    glEnd()
    glPopMatrix()

    # Sirip kiri
    glPushMatrix()
    glTranslatef(0.1, 0.0, -0.2) 
    glRotatef(-45, 1, 0, 0)  
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(1.0, 0.6, 0.0)
    glVertex3f(0.0, 0.0, 0.0)  
    glVertex3f(0.1, 0.05, 0.0)
    glVertex3f(0.15, 0.0, 0.0)
    glVertex3f(0.1, -0.05, 0.0)
    glVertex3f(0.0, -0.1, 0.0)
    glVertex3f(-0.1, -0.05, 0.0)
    glVertex3f(-0.15, 0.0, 0.0)
    glVertex3f(-0.1, 0.05, 0.0)
    glVertex3f(0.0, 0.0, 0.0)  
    glEnd()
    glPopMatrix()

    # Mata kanan
    glPushMatrix()
    glColor3f(0, 0, 0)  # Hitam
    glTranslatef(0.25, 0.05, 0.1)
    eye = gluNewQuadric()
    gluSphere(eye, 0.03, 16, 16)
    gluDeleteQuadric(eye)
    glPopMatrix()

    # Highlight mata kanan
    glPushMatrix()
    glColor3f(1, 1, 1) 
    glTranslatef(0.27, 0.06, 0.11)
    highlight = gluNewQuadric()
    gluSphere(highlight, 0.01, 16, 16)
    gluDeleteQuadric(highlight)
    glPopMatrix()

    # Mata kiri
    glPushMatrix()
    glColor3f(0, 0, 0)
    glTranslatef(0.25, 0.05, -0.1) 
    eye = gluNewQuadric()
    gluSphere(eye, 0.03, 16, 16)
    gluDeleteQuadric(eye)
    glPopMatrix()

    # Highlight mata kiri
    glPushMatrix()
    glColor3f(1, 1, 1) 
    glTranslatef(0.27, 0.06, -0.11) 
    highlight = gluNewQuadric()
    gluSphere(highlight, 0.01, 16, 16)
    gluDeleteQuadric(highlight)
    glPopMatrix()

    glPopMatrix()

def draw_fish2(position):
    "Menggambar ikan kedua yang lebih detail menyerupai ikan blue hippo tang."
    x, y, z = position

    glPushMatrix()
    glTranslatef(x, y, z)

    # Badan ikan
    glPushMatrix()
    glScalef(1.5, 0.9, 0.25)  # Badan berbentuk oval
    glColor3f(0.0, 0.5, 1.0)  # Warna biru
    body = gluNewQuadric()
    gluSphere(body, 0.3, 32, 32)
    gluDeleteQuadric(body)
    glPopMatrix()

    # Pola hitam pada badan
    glPushMatrix()
    glScalef(1.2, 0.6, 1.8)
    glColor3f(0.0, 0.0, 0.0)  # Warna hitam
    glTranslatef(0.0, 0.05, 0.0)
    pattern = gluNewQuadric()
    gluPartialDisk(pattern, 0.15, 0.3, 32, 1, 0, 180)  # Pola setengah lingkaran
    gluDeleteQuadric(pattern)
    glPopMatrix()

    # Ekor kuning (lebih detail dengan lengkungan)
    glPushMatrix()
    glTranslatef(-0.4, 0.0, 0.0)
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(1.0, 1.0, 0.0)  # Warna kuning
    glVertex3f(0.0, 0.0, 0.0)  # Pusat ekor
    for angle in range(0, 361, 45):  # Membuat ekor melengkung
        rad = math.radians(angle)
        glVertex3f(-0.2, 0.1 * math.sin(rad), 0.1 * math.cos(rad))
    glEnd()
    glPopMatrix()

    # Sirip atas (lebih detail dengan lengkungan)
    glPushMatrix()
    glTranslatef(0.0, 0.35, 0.0)  
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(1.0, 1.0, 0.0)  
    glVertex3f(0.0, 0.1, 0.0)  
    glVertex3f(0.05, 0.0, 0.05)
    glVertex3f(0.1, -0.05, 0.0)
    glVertex3f(0.05, -0.1, -0.05)
    glVertex3f(-0.05, -0.1, -0.05)
    glVertex3f(-0.1, -0.05, 0.0)
    glVertex3f(-0.05, 0.0, 0.05)
    glVertex3f(0.0, 0.1, 0.0) 
    glEnd()
    glPopMatrix()

    # Sirip samping (lebih detail dengan lengkungan)
    glPushMatrix()
    glTranslatef(0.15, -0.05, 0.05)
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(1.0, 1.0, 0.0)  # Warna kuning
    glVertex3f(0.0, 0.0, 0.0)  # Pusat sirip
    for angle in range(0, 181, 30):  # Membuat sirip samping melengkung
        rad = math.radians(angle)
        glVertex3f(0.2 * math.cos(rad), 0.0, 0.1 * math.sin(rad))
    glEnd()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.15, -0.05, -0.05)
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(1.0, 1.0, 0.0)  # Warna kuning
    glVertex3f(0.0, 0.0, 0.0)  # Pusat sirip
    for angle in range(0, 181, 30):  # Membuat sirip samping melengkung
        rad = math.radians(angle)
        glVertex3f(0.2 * math.cos(rad), 0.0, -0.1 * math.sin(rad))
    glEnd()
    glPopMatrix()

    # Mata
    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0)  # Hitam
    glTranslatef(0.2, 0.1, 0.05)
    eye = gluNewQuadric()
    gluSphere(eye, 0.03, 16, 16)
    gluDeleteQuadric(eye)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0)  # Hitam
    glTranslatef(0.2, 0.1, -0.05)
    eye = gluNewQuadric()
    gluSphere(eye, 0.03, 16, 16)
    gluDeleteQuadric(eye)
    glPopMatrix()

    # Highlight mata
    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)  # Putih
    glTranslatef(0.22, 0.12, 0.07)
    highlight = gluNewQuadric()
    gluSphere(highlight, 0.01, 8, 8)
    gluDeleteQuadric(highlight)
    glPopMatrix()

    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)  # Putih
    glTranslatef(0.22, 0.12, -0.07)
    highlight = gluNewQuadric()
    gluSphere(highlight, 0.01, 8, 8)
    gluDeleteQuadric(highlight)
    glPopMatrix()

    glPopMatrix()

def draw_coral_reef(position):
    "Menggambar terumbu karang."

    x, y, z = position

    # Memindahkan Terumbu Karang ke posisi yang ditentukan
    glPushMatrix()
    glTranslatef(x, y, z)

    # Membuat dasar terumbu karang (silinder untuk tampilan yang lebih alami)
    base_positions = [
        (0.0, 0.0, 0.0),
        (0.3, 0.1, -0.2),
        (-0.3, 0.1, 0.2),
        (0.2, 0.0, 0.3),
        (-0.2, 0.0, -0.3),
    ]
    for bx, by, bz in base_positions:
        glPushMatrix()
        glTranslatef(bx, by, bz)
        glRotatef(90, 1, 0, 0) 
        glColor3f(0.6, 0.4, 0.3)  # Warna coklat muda untuk dasar terumbu karang
        base = gluNewQuadric()
        gluCylinder(base, 0.2, 0.15, 0.4, 16, 16)  # Silinder 
        gluDeleteQuadric(base)
        glPopMatrix()

    # Membuat cabang-cabang terumbu karang (silinder kecil untuk tampilan yang lebih alami)
    branch_positions = [
        (0.2, 0.4, 0.1),
        (-0.3, 0.5, -0.2),
        (0.1, 0.6, -0.3),
        (-0.2, 0.7, 0.2),
        (0.3, 0.8, -0.1),
        (-0.4, 0.9, 0.3),
    ]
    for bx, by, bz in branch_positions:
        glPushMatrix()
        glTranslatef(bx, by, bz)
        glRotatef(45, 1, 0, 0) 
        glColor3f(0.8, 0.4, 0.3)  # Warna coklat muda untuk cabang-cabang
        branch = gluNewQuadric()
        gluCylinder(branch, 0.05, 0.0, 0.6, 16, 16)  # Cabang berbentuk kerucut
        gluDeleteQuadric(branch)
        glPopMatrix()

    # Membuat ujung-ujung cabang terumbu karang (fan untuk tampilan yang lebih alami)
    for bx, by, bz in branch_positions:
        glPushMatrix()
        glTranslatef(bx, by + 0.6, bz)  # Posisi di ujung cabang
        glColor3f(1.0, 0.5, 0.4)  # Warna lebih terang untuk ujung cabang
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0.0, 0.1, 0.0) 
        for angle in range(0, 361, 45):  # Membuat fan melingkar
            rad = math.radians(angle)
            glVertex3f(0.1 * math.cos(rad), 0.0, 0.1 * math.sin(rad))
        glEnd()
        glPopMatrix()

    # Membuat cabang-cabang kecil (silinder kecil untuk tampilan yang lebih alami)
    small_branch_positions = [
        (0.1, 0.3, 0.2),
        (-0.2, 0.4, -0.1),
        (0.0, 0.5, 0.0),
        (0.2, 0.6, -0.2),
    ]
    for bx, by, bz in small_branch_positions:
        glPushMatrix()
        glTranslatef(bx, by, bz)
        glRotatef(30, 1, 1, 0) 
        glColor3f(0.9, 0.5, 0.4)  # Warna lebih terang untuk cabang-cabang kecil
        branch = gluNewQuadric()
        gluCylinder(branch, 0.03, 0.0, 0.4, 16, 16) # Cabang kecil berbentuk kerucut
        gluDeleteQuadric(branch)
        glPopMatrix()

    # Membuat ujung-ujung cabang kecil (fan untuk tampilan yang lebih alami)
    for bx, by, bz in small_branch_positions:
        glPushMatrix()
        glTranslatef(bx, by + 0.4, bz) 
        glColor3f(1.0, 0.6, 0.5)  # Warna lebih terang untuk ujung cabang kecil
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0.0, 0.05, 0.0)  # Pusat fan
        for angle in range(0, 361, 45):  # Membuat fan melingkar
            rad = math.radians(angle)
            glVertex3f(0.05 * math.cos(rad), 0.0, 0.05 * math.sin(rad))
        glEnd()
        glPopMatrix()

    glPopMatrix()


def draw_aquarium():
    "Menggambar akuarium dengan efek kaca."
    glEnable(GL_BLEND)  # Aktifkan blending untuk transparansi
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glColor4f(0.5, 0.7, 1.0, 0.2)  # Biru muda dengan transparansi
    glLineWidth(3)

    # Definisikan titik-titik akuarium
    vertices = [
        (-5, -5, -5), (8, -5, -5),
        (8, 2, -5), (-5, 2, -5),
        (-5, -5, 5), (8, -5, 5),
        (8, 2, 5), (-5, 2, 5)
    ]

    # Gambar tepi-tepi akuarium
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    # Nonaktifkan depth mask untuk wajah transparan
    glDepthMask(GL_FALSE)

    # Gambar wajah transparan akuarium
    faces = [
        (0, 1, 5, 4),  # Bawah
        (2, 3, 7, 6),  # Atas
        (0, 3, 7, 4),  # Kiri
        (1, 2, 6, 5),  # Kanan
        (0, 1, 2, 3),  # Depan
        (4, 5, 6, 7)   # Belakang
    ]

    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

    # Aktifkan kembali depth mask
    glDepthMask(GL_TRUE)

    glDisable(GL_BLEND)  # Nonaktifkan blending setelah menggambar


def draw_sand():
    "Menggambar pasir dengan elevasi yang telah ditentukan untuk menutupi dasar akuarium."
    glPushMatrix()
    glColor3f(0.9, 0.8, 0.5)  # Warna seperti pasir (kuning kecoklatan terang)

    # Definisikan ukuran grid dan jarak untuk mencocokkan dasar akuarium
    grid_size_x = 27  # Jumlah sel grid sepanjang sumbu x (-5 hingga 8)
    grid_size_z = 21  # Jumlah sel grid sepanjang sumbu z (-5 hingga 5)
    spacing = 0.5

    # Ketinggian yang telah ditentukan untuk permukaan pasir dengan elevasi lebih besar
    heights = [
        [-0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.2, 0.1, 0.0, -0.1, -0.2, -0.3] * 2,
        [-0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1, 0.0, -0.1, -0.2] * 2,
        [-0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0, -0.1] * 2,
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0] * 2,
        [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1] * 2,
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0] * 2,
        [-0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0, -0.1] * 2,
        [-0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1, 0.0, -0.1, -0.2] * 2,
        [-0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.2, 0.1, 0.0, -0.1, -0.2, -0.3] * 2,
    ]

    # Hasilkan permukaan pasir menggunakan grid titik
    for i in range(grid_size_x - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(grid_size_z):
            # Definisikan dua titik untuk strip
            glVertex3f(-5 + i * spacing, -5 + heights[i % len(heights)][j % len(heights[0])], -5 + j * spacing)
            glVertex3f(-5 + (i + 1) * spacing, -5 + heights[(i + 1) % len(heights)][j % len(heights[0])], -5 + j * spacing)
        glEnd()

    glPopMatrix()

def draw_seaweed(base_x=0.0, base_y=0.0, base_z=0.0, height=1.5, segments=15):
    "Menggambar rumput laut"
    glColor3f(0.0, 0.8, 0.3)
    glLineWidth(7)


    current_time = time.time()

    # Batang utama
    glBegin(GL_LINE_STRIP)
    for i in range(segments + 1):
        t = i / segments
        y = t * height

        wave = 0.05 * math.sin(current_time * 2 + y * 10)
        x = base_x + wave
        glVertex3f(x + wave, base_y + y, base_z)
    glEnd()

    glBegin(GL_LINE_STRIP)
    for i in range(segments + 1):
        t = i / segments
        y = t * height

        wave = 0.02 * math.sin(current_time * 4 + y * 10)
        x = base_x + wave
        glVertex3f(x + wave + 0.1, base_y + y, base_z)
    glEnd()

    glBegin(GL_LINE_STRIP)
    for i in range(segments + 1):
        t = i / segments
        y = t * height

        wave = 0.01 * math.sin(current_time * 4 + y * 10)
        x = base_x + wave
        glVertex3f(x + wave + -0.2, base_y + y, base_z)
    glEnd()

    #cabang kecil kiri kanan
    for i in range(2, segments, 4):
        t = i / segments
        y = t * height
        wave = 0.03 * math.sin(current_time * 2 + y * 10)
        x = base_x + wave
        leaf_length = 0.07

        glBegin(GL_LINES)
        glVertex3f(x, base_y + y, base_z)
        glVertex3f(x + leaf_length, base_y + y + 0.05, base_z + 0.02)
        glEnd()

        glBegin(GL_LINES)
        glVertex3f(x, base_y + y, base_z)
        glVertex3f(x - leaf_length, base_y + y + 0.1, base_z - 0.02)
        glEnd()

def draw_rock(x=0.0, y=0.0, z=0.0, scale=0.2):
    "Menggambar batu di dasar akuarium."
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(1.0, 0.5, 1.0)
    glColor3f(0.4, 0.4, 0.4)
    quad = gluNewQuadric()
    gluSphere(quad, scale, 16, 16)
    gluDeleteQuadric(quad)
    glPopMatrix()

def draw_seaweed_with_rocks(base_x, base_y, base_z):
    "Menggambar rumput laut dengan batu di sekitarnya."
    draw_seaweed(base_x, base_y, base_z)

    draw_rock(base_x - 0.2, base_y, base_z)
    draw_rock(base_x + 0.2, base_y, base_z)
    draw_rock(base_x, base_y, base_z + 0.2)

# Membuat gelembung
class Bubble:
    def __init__(self):
        self.x = random.uniform(-5.0, 8.5)
        self.y = random.uniform(-5.0, 1)
        self.z = random.uniform(-5.0, 5)
        self.radius = random.uniform(0.1, 0.25)
        self.speed = random.uniform(0.001, 0.01)
        
    def update(self):
        self.y += self.speed
        if self.y > 3.0:
            self.y = random.uniform(-4.0, -2.0)

#Buat beberapa gelembung
bubbles = [Bubble() for _ in range(15)]

running = True
mouse_down = False
last_mouse_pos = (0, 0)
angle = 0

# Variabel untuk pusat rotasi kamera
center_x, center_y, center_z = 0.0, 0.0, 0.0
right_mouse_down = False  # Melacak status tombol kanan mouse

# Tambahkan posisi untuk beberapa ikan
fish_positions = [
    (-2, 0, -2),
    (-3, -1, 2),
    (1, -2, -3),
    (3, 0, 1),
    (0, 1, -3)  # Posisi untuk ikan kedua
]

# Kurangi kecepatan untuk pergerakan yang lebih lambat
fish_velocities = [(random.uniform(-0.005, 0.005), random.uniform(-0.005, 0.005), random.uniform(-0.005, 0.005)) for _ in fish_positions]

# Daftar untuk menyimpan posisi makanan
food_positions = []

# Daftar untuk menyimpan posisi makanan yang mengapung
floating_food_positions = []

# Daftar untuk menyimpan ukuran ikan
fish_sizes = [1.0 for _ in fish_positions]

# Fungsi untuk memperbarui posisi ikan dan membuat mereka bergerak menuju makanan terdekat
def update_fish_positions():
    global fish_positions, fish_velocities, food_positions, floating_food_positions
    for i in range(len(fish_positions)):
        x, y, z = fish_positions[i]
        vx, vy, vz = fish_velocities[i]

        # Gabungkan makanan yang mengapung dan jatuh ke dalam satu daftar
        all_food_positions = food_positions + floating_food_positions

        # Periksa apakah ada makanan
        if all_food_positions:
            # Temukan makanan terdekat (mengapung atau jatuh)
            nearest_food = min(all_food_positions, key=lambda food: math.sqrt((food[0] - x)**2 + (food[1] - y)**2 + (food[2] - z)**2))
            fx, fy, fz = nearest_food

            # Hitung arah menuju makanan
            direction_x = fx - x
            direction_y = fy - y
            direction_z = fz - z
            magnitude = math.sqrt(direction_x**2 + direction_y**2 + direction_z**2)

            # Normalisasi dan atur kecepatan menuju makanan
            if magnitude > 0:
                vx = (direction_x / magnitude) * 0.01  # Sesuaikan kecepatan
                vy = (direction_y / magnitude) * 0.01
                vz = (direction_z / magnitude) * 0.01

        # Perbarui posisi
        x += vx
        y += vy
        z += vz

        # Jaga agar ikan tetap dalam batas akuarium
        if x < -4.5 or x > 7.5:
            vx = -vx
        if y < -4.5 or y > 1.5:
            vy = -vy
        if z < -4.5 or z > 4.5:
            vz = -vz

        # Simpan posisi dan kecepatan yang diperbarui
        fish_positions[i] = (x, y, z)
        fish_velocities[i] = (vx, vy, vz)

# Fungsi untuk memperbarui posisi makanan
def update_food_positions():
    global food_positions
    new_food_positions = []
    for food in food_positions:
        x, y, z = food
        y -= 0.02  # Makanan jatuh ke bawah
        if y > -4.5:  # Jaga agar makanan tetap dalam akuarium
            new_food_positions.append((x, y, z))  # Debugging
    food_positions = new_food_positions

# Fungsi untuk memperbarui posisi makanan yang mengapung
def update_floating_food_positions():
    global floating_food_positions, food_positions
    new_positions = []
    for food in floating_food_positions:
        x, y, z = food
        y -= 0.001  # Turunkan makanan yang mengapung secara bertahap
        if y > 0.0:  # Hentikan penurunan makanan saat mencapai ketinggian tertentu
            new_positions.append((x, y, z))
        else:
            food_positions.append((x, y, z))  # Pindahkan makanan ke keadaan jatuh
    floating_food_positions = new_positions  # Perbarui posisi makanan yang mengapung

# Fungsi untuk memeriksa apakah ikan memakan makanan
def check_fish_eats_food():
    global food_positions, floating_food_positions, fish_sizes
    eaten_food = []  # Daftar untuk menyimpan makanan jatuh yang telah dimakan
    eaten_floating_food = []  # Daftar untuk menyimpan makanan yang mengapung yang telah dimakan
    tolerance = 0.3  # Tentukan toleransi untuk kedekatan

    # Periksa makanan yang jatuh
    for food in food_positions:
        fx, fy, fz = food
        for i, (x, y, z) in enumerate(fish_positions):
            # Periksa apakah ikan cukup dekat dengan makanan
            if abs(x - fx) < tolerance and abs(y - fy) < tolerance and abs(z - fz) < tolerance:
                fish_sizes[i] += 0.1  # Ikan tumbuh
                eaten_food.append(food)  # Tandai makanan sebagai dimakan
                break

    # Periksa makanan yang mengapung
    for food in floating_food_positions:
        fx, fy, fz = food
        for i, (x, y, z) in enumerate(fish_positions):
            # Periksa apakah ikan cukup dekat dengan makanan yang mengapung
            if abs(x - fx) < tolerance and abs(y - fy) < tolerance and abs(z - fz) < tolerance:
                fish_sizes[i] += 0.1  # Ikan tumbuh
                eaten_floating_food.append(food)  # Tandai makanan yang mengapung sebagai dimakan
                break

    # Hapus makanan yang dimakan dari daftar masing-masing
    food_positions = [food for food in food_positions if food not in eaten_food]
    floating_food_positions = [food for food in floating_food_positions if food not in eaten_floating_food]


# Fungsi untuk menggambar indikator jatuhnya makanan
def draw_food_indicator(mx, my):
    # Konversi koordinat layar ke koordinat dunia
    fx = (mx / width) * 13 - 5  # Peta ke rentang x akuarium (-5 hingga 8)
    fz = (my / height) * 10 - 5  # Peta ke rentang z akuarium (-5 hingga 5)
    glPushMatrix()
    glTranslatef(fx, 1.5, fz)
    glColor4f(1.0, 0.0, 0.0, 0.5)  # Warna merah transparan untuk indikator
    quad = gluNewQuadric()
    gluSphere(quad, 0.15, 16, 16)
    gluDeleteQuadric(quad)
    glPopMatrix()

# Fungsi untuk menggambar ikan menghadap arah gerakannya
def draw_fish_with_direction(position, velocity, draw_function, size):
    x, y, z = position
    vx, vy, vz = velocity

    # Hitung sudut untuk menghadap arah gerakan
    if vx == 0 and vz == 0:  # Hindari pembagian dengan nol
        angle_y = 0
    else:
        angle_y = math.degrees(math.atan2(-vz, vx))  # Sudut yaw (rotasi sekitar sumbu Y)

    if vx == 0 and vz == 0 and vy == 0:  # Hindari pembagian dengan nol
        angle_x = 0
    else:
        angle_x = math.degrees(math.atan2(vy, math.sqrt(vx**2 + vz**2)))  # Sudut pitch (rotasi sekitar sumbu X)

    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(angle_y, 0, 1, 0)  # Rotasi sekitar sumbu Y (yaw)
    glRotatef(angle_x, 0, 0, 0)  # Rotasi sekitar sumbu X (pitch)
    glScalef(size, size, size)  # Skala ikan berdasarkan ukurannya
    draw_function((0, 0, 0))  # Gambar ikan di titik asal
    glPopMatrix()

# Tambahkan posisi untuk terumbu karang
coral_positions = [
    (-4, -4.4, -4),
    (7, -4, 4),
    (0, -4, 0)
]

# Tambahkan posisi untuk terumbu karang
coral_reef_position = (2, -4, 4.5)  # Dekat dasar akuarium

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  
                radius -= 1
                radius = max(1.0, radius)  # Radius minimum
            elif event.button == 5:  
                radius += 1
                radius = min(50.0, radius)  # Radius maksimum
            elif event.button == 1: 
                mouse_down = True
                last_mouse_pos = pygame.mouse.get_pos()
            elif event.button == 3: 
                right_mouse_down = True
                last_mouse_pos = pygame.mouse.get_pos()
            elif event.button == 2:  # Tombol tengah mouse untuk menjatuhkan makanan
                mx, my = pygame.mouse.get_pos()
                # Konversi koordinat layar ke koordinat dunia
                fx = (mx / width) * 13 - 5  # Peta ke rentang x akuarium (-5 hingga 8)
                fz = (my / height) * 10 - 5  # Peta ke rentang z akuarium (-5 hingga 5)
                floating_food_positions.append((fx, 1.5, fz))  # Tambahkan makanan mengapung di atas

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: 
                mouse_down = False
            elif event.button == 3: 
                right_mouse_down = False

        if event.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            dx = x - last_mouse_pos[0]
            dy = y - last_mouse_pos[1]

            if mouse_down:  # Putar kamera
                angle_x += dx * 0.3
                angle_y += dy * 0.3
                angle_y = max(min(angle_y, 89), -89)
            elif right_mouse_down:  # Pindahkan titik pusat
                center_x += dx * 0.01
                center_y -= dy * 0.01

            last_mouse_pos = (x, y)

    # Perbarui posisi ikan
    update_fish_positions()

    # Perbarui posisi makanan
    update_food_positions()

    # Perbarui posisi makanan yang mengapung
    update_floating_food_positions()

    # Periksa apakah ikan memakan makanan
    check_fish_eats_food()

    # Hitung posisi kamera
    camX = math.sin(math.radians(angle_x)) * math.cos(math.radians(angle_y)) * radius
    camY = math.sin(math.radians(angle_y)) * radius
    camZ = math.cos(math.radians(angle_x)) * math.cos(math.radians(angle_y)) * radius

    # Bersihkan dan atur ulang tampilan
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()

    # Sesuaikan perspektif berdasarkan radius
    gluPerspective(60, (width / height), 0.1, max(100.0, radius + 10.0))
    gluLookAt(camX, camY, camZ, center_x, center_y, center_z, 0, 1, 0)

    # Perbarui posisi cahaya secara dinamis agar tetap di tengah akuarium
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    plant_positions = [(-1.5, -5, -4), (-2, -4.5, 2), (6, -4.9, 1)]
    for pos in plant_positions:
        glPushMatrix()
        draw_seaweed_with_rocks(*pos)
        glPopMatrix()

    # Gambar adegan
    draw_aquarium()
    draw_sand()

    # Gambar terumbu karang
    draw_coral_reef(coral_reef_position)

    # Gambar makanan
    for food in food_positions:
        fx, fy, fz = food
        glPushMatrix()
        glTranslatef(fx, fy, fz)
        glColor3f(1.0, 0.8, 0.0)  # Warna kekuningan untuk makanan
        quad = gluNewQuadric()
        gluSphere(quad, 0.1, 16, 16)
        gluDeleteQuadric(quad)
        glPopMatrix()

    # Gambar makanan yang mengapung
    for food in floating_food_positions:
        fx, fy, fz = food
        glPushMatrix()
        glTranslatef(fx, fy, fz)
        glColor3f(1.0, 0.8, 0.0)  # Warna kekuningan untuk makanan
        quad = gluNewQuadric()
        gluSphere(quad, 0.1, 16, 16)
        gluDeleteQuadric(quad)
        glPopMatrix()

    # Gambar indikator jatuhnya makanan
    mx, my = pygame.mouse.get_pos()
    draw_food_indicator(mx, my)

    # Gambar semua ikan dengan arah dan ukuran
    for i, position in enumerate(fish_positions):
        velocity = fish_velocities[i]
        size = fish_sizes[i]
        if i % 2 == 0:  # Bergantian antara draw_fish dan draw_fish2
            draw_fish_with_direction(position, velocity, draw_fish, size)
        else:
            draw_fish_with_direction(position, velocity, draw_fish2, size)

    # Gambar semua terumbu karang
    for position in coral_positions:
        draw_coral_reef(position)

    for bubble in bubbles:
        bubble.update()

        if bubble.y < 1.7:
            glEnable(GL_BLEND)  # Aktifkan blending untuk transparansi
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            quad = gluNewQuadric()
            glPushMatrix()
            glTranslatef(bubble.x, bubble.y, bubble.z)
            glColor4f(1.0, 1.5, 5.0, 0.6)
            gluSphere(quad, bubble.radius, 16, 16)
            gluDeleteQuadric(quad)
            glPopMatrix()

    angle += 0.01

    pygame.display.flip()

pygame.quit()