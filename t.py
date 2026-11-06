import pygame as pg
from time import time
from math import *

pg.init()

display = pg.display.set_mode((700, 500))
fps = 60
clock = pg.time.Clock()

class Vector3():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):

        if type(other) == type(1) or type(other) == type(0.5):
            return Vector3(self.x * other, self.y * other, self.z * other)

        return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __rmul__(self, other):

        return self.__mul__(other)

    def __truediv__(self, other):

        if type(other) == type(1) or type(other) == type(0.5):
            return Vector3(self.x / other, self.y / other, self.z / other)
        
        return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)

    def length(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):

        cx = self.y * other.z - self.z * other.y
        cy = self.z * other.x - other.x * self.z
        cz = self.x * other.y - other.y * self.x

        return Vector3(cx, cy, cz)

def sign(x):

    if x == 0:
        return 0
    if x > 0:
        return 1
    if x < 0:
        return - 1 

class Vector2():
    def __init__(self, x, y):
        self.x = x
        self.y = y

vertices = [
    Vector3(0, 0, 0),
    Vector3(1, 0, 0),
    Vector3(0, 1, 0),
    Vector3(1, 1, 0),
    Vector3(0, 0, 1),
    Vector3(1, 0, 1),
    Vector3(0, 1, 1),
    Vector3(1, 1, 1)
]

lines = [
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
    (0, 1),
    (1, 3),
    (0, 2),
    (3, 2),
    (4, 5),
    (5, 7),
    (7, 6),
    (4, 6)
]

scale = 100

nearPlane = 100

renderables = []

def getTriangleZ(indices, vecs, pos):

    return sum(vecs[i].z for i in indices) / len(indices)

def isFrontFacing(v1, v2, v3):
            
    return (v2[0] - v1[0]) * (v3[1] - v1[1]) - (v2[1] - v1[1]) * (v3[0] - v1[0]) < 0

class Cube():

    def __init__(self):

        self.size = Vector3(1, 1, 1)
        self.position = Vector3(0, 0, 0)
        self.prevPos = self.position
        self.acceleration = Vector3(0, 0, 0)

        self.renderedVerts = []
        self.Verts = []

        renderables.append(self)

    def getFaceData(self):

        RENDEREDverts = self.renderedVerts

        baseColor = Vector3(255, 150, 150)
        
        frontFace = Vector3(0, 0, -1)
        topFace = Vector3(0, 1, 0)
        bottomFace = Vector3(0, -1, 0)
        rightFace = Vector3(1, 0, 0)
        leftFace = Vector3(-1, 0, 0)

        sunDirection = Vector3(0.8, 1, -0.4)

        topUVerts = (RENDEREDverts[2], RENDEREDverts[3], RENDEREDverts[6])
        topLVerts = (RENDEREDverts[3], RENDEREDverts[6], RENDEREDverts[7])

        rightUVerts = (RENDEREDverts[1], RENDEREDverts[5], RENDEREDverts[7])
        rightLVerts = (RENDEREDverts[1], RENDEREDverts[3], RENDEREDverts[7])

        frontUVerts = (RENDEREDverts[0], RENDEREDverts[1], RENDEREDverts[2])
        frontLVerts = (RENDEREDverts[2], RENDEREDverts[1], RENDEREDverts[3])

        bottomUVerts = (RENDEREDverts[0], RENDEREDverts[1], RENDEREDverts[4])
        bottomLVerts = (RENDEREDverts[1], RENDEREDverts[4], RENDEREDverts[5])

        leftUVerts = (RENDEREDverts[4], RENDEREDverts[0], RENDEREDverts[6])
        leftLVerts = (RENDEREDverts[6], RENDEREDverts[2], RENDEREDverts[0])

        topUZ = getTriangleZ((2, 3, 6), self.Verts, self.position)
        topLZ = getTriangleZ((3, 6, 7), self.Verts, self.position)
        bottomUZ = getTriangleZ((0, 1, 4), self.Verts, self.position)
        bottomLZ = getTriangleZ((1, 4, 5), self.Verts, self.position)
        rightUZ = getTriangleZ((1, 5, 7), self.Verts, self.position)
        rightLZ = getTriangleZ((1, 3, 7), self.Verts, self.position)
        frontUZ = getTriangleZ((0, 1, 2), self.Verts, self.position)
        frontLZ = getTriangleZ((2, 1, 3), self.Verts, self.position)
        leftUZ = getTriangleZ((4, 0, 6), self.Verts, self.position)
        leftLZ = getTriangleZ((6, 2, 0), self.Verts, self.position)

        faceData = []

        ambient = 0.2

        dot = topFace.dot(sunDirection)
        topShading = baseColor * min(max(dot, ambient), 1)

        dot = rightFace.dot(sunDirection)
        rightShading = baseColor * min(max(dot, ambient), 1)

        dot = bottomFace.dot(sunDirection)
        bottomShading = baseColor * min(max(dot, ambient), 1)

        dot = frontFace.dot(sunDirection)
        frontShading = baseColor * min(max(dot, ambient), 1)

        dot = leftFace.dot(sunDirection)
        leftShading = baseColor * min(max(dot, ambient), 1)

        if isFrontFacing(topUVerts[0], topUVerts[1], topUVerts[2]):
            faceData.append((topUVerts, topShading, topUZ))
        if not isFrontFacing(topLVerts[0], topLVerts[1], topLVerts[2]):
            faceData.append((topLVerts, topShading, topLZ))

        if not isFrontFacing(bottomUVerts[0], bottomUVerts[1], bottomUVerts[2]):
            faceData.append((bottomUVerts, bottomShading, bottomUZ))
        if isFrontFacing(bottomLVerts[0], bottomLVerts[1], bottomLVerts[2]):
            faceData.append((bottomLVerts, bottomShading, bottomLZ))

        if isFrontFacing(rightUVerts[0], rightUVerts[1], rightUVerts[2]):
            faceData.append((rightUVerts, rightShading, rightUZ))
        if not isFrontFacing(rightLVerts[0], rightLVerts[1], rightLVerts[2]):
            faceData.append((rightLVerts, rightShading, rightLZ))

        if isFrontFacing(frontUVerts[0], frontUVerts[1], frontUVerts[2]):
            faceData.append((frontUVerts, frontShading, frontUZ))
        if isFrontFacing(frontLVerts[0], frontLVerts[1], frontLVerts[2]):
            faceData.append((frontLVerts, frontShading, frontLZ))

        if isFrontFacing(leftUVerts[0], leftUVerts[1], leftUVerts[2]):
            faceData.append((leftUVerts, leftShading, leftUZ))
        if not isFrontFacing(leftLVerts[0], leftLVerts[1], leftLVerts[2]):
            faceData.append((leftLVerts, leftShading, leftLZ))

        return faceData

    def render(self):

        RENDEREDverts = []
        vectors = []
        OGvectors = []
    
        for vec in vertices:
    
            x = vec.x + self.position.x
            y = 1 - (vec.y + self.position.y)
            z = (vec.z + self.position.z) * 0.25
    
            x *= scale
            y *= scale
    
            z += 0.5
    
            if z == 0:
                z = 0.0001
    
                z = 1 / z
            else:
    
                z = 1 / z
    
            pos = ((x * z + 350), (y * z + 250))
    
            vector = Vector3(pos[0], 1 - pos[1], z)
    
            #pg.draw.circle(display, (255, 255, 255), (pos[0] + (10 * z) / 2, pos[1] + (10 * z) / 2), 10 * z)
            RENDEREDverts.append(pos)
            vectors.append(vector)
            OGvectors.append(Vector3(x, y, z))

        self.renderedVerts = RENDEREDverts
        self.Verts = OGvectors

        for line in lines:
    
            outOfBounds = False
    
            x1 = OGvectors[line[0]].x
            y1 = OGvectors[line[0]].y
            z1 = OGvectors[line[0]].z
    
            x2 = OGvectors[line[1]].x
            y2 = OGvectors[line[1]].y
            z2 = OGvectors[line[1]].z
    
            finalVector1 = Vector2((x1 * z1 + 350), (y1 * z1 + 250))
            finalVector2 = Vector2((x2 * z2 + 350), (y2 * z2 + 250))
    
            if z1 < 0:
                outOfBounds = True
    
                z = nearPlane
    
                x1 = (x1 * z + 350)
                y1 = (y1 * z + 250)
    
                finalVector1 = Vector2(x1, y1)
                
            if z2 < 0:
                if outOfBounds == True: continue
    
                z = nearPlane
                
                x2 = (x2 * z + 350)
                y2 = (y2 * z + 250)
    
                finalVector2 = Vector2(x2, y2)
    
            #pg.draw.aaline(display, (255, 255, 255), (finalVector1.x, finalVector1.y), (finalVector2.x, finalVector2.y), 2)

    def applyForces(self):

        dt = (1 / 30)

        self.acceleration += Vector3(0, -9.81 * dt, 0)

        if pg.mouse.get_pressed()[0] == True:
            mousePos = pg.mouse.get_pos()
            mousePos = Vector3((mousePos[0] - 350) / scale, (1 -(mousePos[1] - 250)) / scale, 10)

            direction = mousePos - self.position

            direction = direction / direction.length()

            self.acceleration += direction * 3


    def verlet(self):

        dt = (1 / 30)

        current = 2 * self.position - self.prevPos + self.acceleration * (dt * dt)

        self.prevPos = self.position
        self.position = current
        self.acceleration = Vector3(0, 0, 0)

    def getAABB(self):

        minC = self.position - (self.size / 2)
        maxC = self.position + (self.size / 2)

        return minC, maxC

    def collisionCheck(self):

        for cube in renderables:

            bPos = cube.position
            aPos = self.position

            normal = Vector3(0, 0, 0)

            minA, maxA = self.getAABB()
            minB, maxB = cube.getAABB()

            overlap_x = min(maxA.x, maxB.x) - max(minA.x, minB.x)
            overlap_y = min(maxA.y, maxB.y) - max(minA.y, minB.y)
            overlap_z = min(maxA.z, maxB.z) - max(minA.z, minB.z)


            if overlap_x > 0 and overlap_y > 0 and overlap_z > 0:

                colNormal = bPos - aPos

                penetrationDepth = min(overlap_x, overlap_y, overlap_z)

                if overlap_x == penetrationDepth:
                    normal += Vector3(sign(colNormal.x), 0, 0)
                if overlap_y == penetrationDepth:
                    normal += Vector3(0, sign(colNormal.y), 0)
                if overlap_z == penetrationDepth:
                    normal += Vector3(0, 0, sign(colNormal.z))

                v1 = self.position - self.prevPos
                v2 = cube.position - cube.prevPos
                relVel = v2 - v1

                tangentLength = relVel.length()

                if tangentLength > 0:

                    frictionCoeff = 0.2
                    frictionNormal = (relVel / tangentLength) * frictionCoeff

                    normal -= frictionNormal
                    

                self.position -= normal * penetrationDepth * 0.5
                cube.position += normal * penetrationDepth * 0.5

    def physUpdate(self):

        self.applyForces()

        if self.position.y < -5:
            self.position.y = -5

        self.collisionCheck()

        self.verlet()


for i in range(10):
    c = Cube()
    c.position = Vector3(0, i, 10)
    c.prevPos = c.position

while True:

    display.fill((0, 0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    lordVerity = []

    for cube in renderables:
        cube.physUpdate()
        cube.render()
        lordVerity.extend(cube.getFaceData())

    lordVerity.sort(key=lambda face: face[2])

    for verts, color, depth in lordVerity:

        pg.draw.polygon(display, (color.x, color.y, color.z), verts)

    pg.display.update()
    clock.tick(fps)