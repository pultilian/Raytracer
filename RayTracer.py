import numpy as np
import math as math


class Ray:
    def __init__(self, originPoint, directionVector):
        self.originPoint = originPoint
        self.directionVector = directionVector

    def printPoint(self):
        print(self.originPoint)

    def determineRayPoint(self,distance):
        return self.originPoint + np.dot(distance,self.directionVector)


class Object():
    def __init__(self):
        self.color = Color(0,0,0,0)

    def intersect(self, ray):
        pass

class Triangle(Object):
    def __init__(self, a, b, c, color):
        self.VectA = a
        self.VectB = b
        self.VectC = c
        self.color = color
        self.normal = self.calcNormal()

    def calcNormal(self):
        CA = self.VectC.subtract(self.VectA)
        BA = self.VectB.subtract(self.VectA)
        return CA.cross(BA).normalize()

    def distance(self):
        return self.normal.dot(self.VectA)

    def calcNormalAt(self, intersectPos):
        return self.normal

    def intersect(self, ray):
        rayDir = ray.directionVector
        rayOrigin = ray.originPoint


        # edge1 = self.VectB.subtract(self.VectA)
        # edge2 = self.VectC.subtract(self.VectA)
        #
        # h = rayDir.cross(edge2)
        # a = edge1.dot(h)
        #
        # if a > -0.000001 and a < 0.000001:
        #     return -1
        #
        # f = 1/a
        #
        # s = rayOrigin.subtract(self.VectA)
        # u = s.dot(h) * f
        # if u < 0 or u > 1:
        #     return -1
        #
        # q = s.cross(edge1)
        # v = f * (rayDir.dot(q))
        # if v < 0 or v > 1:
        #     return -1
        #
        # t = f * (edge2.dot(q))
        # if t > 0.000001:
        #     newA = rayDir.dot(self.normal)
        #     newB = self.normal.dot(ray.originPoint.add(self.normal.multiply(self.distance()).negative()))
        #     return -1 * newB/newA
        #     # outIntersectionPoint = rayOrigin.add(rayDir.multiply(t))
        #     # add1 = (outIntersectionPoint.x - rayOrigin.x)**2 + (outIntersectionPoint.y - rayOrigin.y)*2 + (outIntersectionPoint.z - rayOrigin.z)**2
        #     # if add1 >= 0:
        #     #     return math.sqrt(add1)
        #     # else:
        #     #     magnitude = math.sqrt(add1 * -1)
        #     #     return magnitude
        # else:
        #     return -1

        # Ray Origin distance to point of intersection
        # distance = self.distance()

        a = rayDir.dot(self.normal)

        if a == 0:
            return -1
        else:
            if a > 0:
                self.normal.negative()
            distance = self.normal.dot(self.VectA)

            dot1 = self.normal.dot(rayOrigin)
            add1 = (dot1 + distance) * -1
            dot2 = self.normal.dot(rayDir)
            t = add1 / dot2

            if t <= 0:
                return -1
            Q = rayOrigin.add(rayDir.multiply(t))

            b = self.normal.dot(ray.originPoint.add(self.normal.multiply(distance).negative()))

            CA = self.VectC.subtract(self.VectA)
            QA = Q.subtract(self.VectA)
            test1 = self.normal.dot(CA.cross(QA))

            BC = self.VectB.subtract(self.VectC)
            QC = Q.subtract(self.VectC)
            test2 = self.normal.dot(BC.cross(QC))

            AB = self.VectA.subtract(self.VectB)
            QB = Q.subtract(self.VectB)
            test3 = self.normal.dot(AB.cross(QB))

            if test1 >=0 and test2 >= 0 and test3 >= 0:
                return t
            else:
                return -1
        # pass

class Sphere(Object):
    def __init__(self, radius, center, color):
        self.radius = radius
        self.center = center
        self.color = color

    def calcNormal(self, point):
        return

    def calcNormalAt(self, intersectPos):
        Vector = intersectPos.add(self.center.negative()).normalize()
        return Vector

    def intersect(self, ray):
        rayOrigin = ray.originPoint
        rayOriginX = rayOrigin.x
        rayOriginY = rayOrigin.y
        rayOriginZ = rayOrigin.z

        rayDir = ray.directionVector
        rayDirX = rayDir.x
        rayDirY = rayDir.y
        rayDirZ = rayDir.z

        sphCent = self.center
        sphCentX = sphCent.x
        sphCentY = sphCent.y
        sphCentZ = sphCent.z

        B = 2*((rayOriginX - sphCentX)*rayDirX + (rayOriginY - sphCentY)*rayDirY + (rayOriginZ - sphCentZ)*rayDirZ)
        C = ((rayOriginX - sphCentX)**2 + (rayOriginY - sphCentY)**2 + (rayOriginZ - sphCentZ)**2) - self.radius**2

        discriminant = B ** 2 - 4 * C
        if discriminant < 0:
            return -1

        t1 = (-B + math.sqrt(discriminant)) / 2
        t2 = (-B - math.sqrt(discriminant)) / 2
        if t1 > 0 and t2 > 0:
            if t1 < t2:
                return t1
            else:
                return t2
        elif t1 <= 0 and t2 > 0:
            return t2
        elif t2 <= 0 and t1 > 0:
            return t1
        else:
            return -1


class Color:
    def __init__(self,r,g,b,special):
        self.r = r
        self.g = g
        self.b = b
        self.special = special

    def toString(self):
        return (str(int(self.r * 255)) + " " + str(int(self.g * 255)) + " " + str(int(self.b * 255)) + " ")

    def brightness(self):
        return (self.r + self.g + self.b)/3

    def scaleColor(self, c):
        return Color(self.r * c, self.g * c, self.b * c, self.special)

    def add(self, color):
        return Color(self.r + color.r, self.g + color.g, self.b + color.b, self.special)

    def multiply(self, color):
        return Color(self.r * color.r, self.g * color.g, self.b * color.b, self.special)

    def average(self, color):
        return Color((self.r + color.r)/2, (self.g + color.g)/2, (self.b + color.b)/2, self.special)

    def clip(self):
        allLight = self.r + self.g + self.b
        excessLight = allLight - 3
        if(excessLight > 0):
            self.r = self.r + excessLight * (self.r/allLight)
            self.g = self.g + excessLight * (self.g / allLight)
            self.b = self.b + excessLight * (self.b / allLight)
        if self.r > 1:
            self.r = 1
        if self.g > 1:
            self.g = 1
        if self.b > 1:
            self.b = 1
        if self.r < 0:
            self.r = 0
        if self.g < 0:
            self.g = 0
        if self.b < 0:
            self.b = 0

        return Color(self.r, self.g, self.b, self.special)


class Light:
    def __init__(self, position, color):
        self.position = position
        self.color = color

class Camera:
    def __init__(self, position, direction, right, down):
        self.position = position
        self.direction = direction
        self.right = right
        self.down = down

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def magnitude(self):
        return math.sqrt((self.x**2) + (self.y**2) + (self.z**2))

    def normalize(self):
        magnitude = self.magnitude()
        if magnitude != 0:
            return Vector(self.x / magnitude, self.y / magnitude, self.z / magnitude)
        else:
            return self

    def negative(self):
        return Vector(-self.x, -self.y, -self.z)

    def dot(self, vector):
        return (self.x * vector.x) + (self.y * vector.y) + (self.z*vector.z)

    def cross(self, vector):
        return Vector(self.y*vector.z - self.z*vector.y,
                      self.z * vector.x - self.x * vector.z,
                      self.x * vector.y - self.y * vector.x)

    def add(self, vector):
        return Vector(self.x + vector.x, self.y + vector.y, self.z + vector.z)

    def multiply(self, c):
        return Vector(self.x*c, self.y*c, self.z*c)

    def subtract(self, vector):
        return Vector(self.x - vector.x, self.y - vector.y, self.z - vector.z)

class RayTracer:
    def __init__(self):
        self.camPosition = Vector(0,0,1)
        self.rays = []
        pass

    def getColorAt(self, intersectPos, intersectDir, objects, bestIndex, accuracy, ambientLight, light, depth, phongConstant):
        bestObjectColor = objects[bestIndex].color
        bestObjectNormal = objects[bestIndex].calcNormalAt(intersectPos)
        final_color = bestObjectColor.scaleColor(ambientLight)
        D = intersectDir.negative()

        if bestObjectColor.special > 1 and depth <= 2:
            dotProduct1 = D.dot(bestObjectNormal)
            scalar1 = bestObjectNormal.multiply(dotProduct1)
            scalar2 = scalar1.multiply(-2)
            add1 = scalar2.add(D)
            reflectionDir = add1.normalize().negative()

            offset = reflectionDir.multiply(0.001)
            relectRay = Ray(intersectPos.add(offset), reflectionDir)

            reflectIntersects = []

            for i in range(len(objects)):
                reflectIntersects.append(objects[i].intersect(relectRay))

            newIndex = self.calcClosestObject(reflectIntersects)

            if newIndex != -1:
                if reflectIntersects[newIndex] > accuracy:
                    reflectIntersectPos = intersectPos.add(reflectionDir.multiply(reflectIntersects[newIndex]))
                    reflectIntersectDir = reflectionDir
                    reflectIntersectColor = self.getColorAt(reflectIntersectPos, reflectIntersectDir, objects, newIndex, accuracy, ambientLight, light, depth + 1, phongConstant)

                    final_color = final_color.add(reflectIntersectColor.scaleColor(bestObjectColor.special - 1))


        lightDir = light.position.add(intersectPos.negative()).normalize()

        cosineAngle = bestObjectNormal.dot(lightDir)

        if cosineAngle > 0:
            inShadow = False
            distanceToLight = light.position.add(intersectPos.negative()).normalize()
            distanceToLightMag = distanceToLight.magnitude()

            shadowRay = Ray(intersectPos, light.position.add(intersectPos.negative()).normalize())
            newIntersections = []

            for i in range(len(objects)):
                if inShadow == False:
                    newIntersections.append(objects[i].intersect(shadowRay))
                else:
                    break
            for i in range(len(newIntersections)):
                if newIntersections[i] > accuracy:
                    if newIntersections[i] <= distanceToLightMag:
                        inShadow = True
                    break

            if inShadow == False:
                final_color = final_color.add(bestObjectColor.multiply(light.color).scaleColor(cosineAngle))

                if (bestObjectColor.special > 0 and bestObjectColor.special <= 1):
                    dotProduct1 = D.dot(bestObjectNormal)
                    scalar1 = bestObjectNormal.multiply(dotProduct1)
                    scalar2 = scalar1.multiply(-2)
                    add1 = scalar2.add(D)
                    reflectionDir = add1.normalize()

                    specular = lightDir.negative().dot(reflectionDir)
                    # specular = reflectionDir.dot(lightDir)
                    if (specular > 0):
                        specular = specular**phongConstant
                        final_color = final_color.add(light.color.scaleColor(specular*bestObjectColor.special))
                    # opposite incoming ray dot Reflection raised to phong all this by specular color

        return final_color.clip()

    def calcClosestObject(self, objects):
        retIndex = 0
        if len(objects) == 0:
            return -1
        elif len(objects) == 1:
            if objects[0] > 0:
                return 0
            else:
                return -1
        else:
            max = math.inf
            for i in range(len(objects)):
                if max > objects[i] and objects[i] > 0:
                    max = objects[i]
                    retIndex = i

            if max != math.inf:
                return retIndex
            else:
                return -1

    def rayTree(self):
        pass

    def main(self):
        bgColor = Color(.1,.1,.1, 0)
        camPosition = Vector(0,0,1)
        lookAt = Vector(0,0,0)
        difference = camPosition.subtract(lookAt)
        camDir = difference.negative().normalize()
        camRight = Vector(1,0,0).cross(camDir).normalize()
        camDown = camRight.cross(camDir)
        camera = Camera(camPosition,camDir,camRight,camDown)

        light = Light(Vector(2,-2,2), Color(1,1,1, 0))
        ambientLight = .15
        accuracy = 0.000001

        pixels = []

        width = 500
        height = 500

        objects = []

        objects.append(Sphere(.2, Vector(0,0,0), Color(.1,.1,.1, 2)))
        objects.append(Sphere(.1, Vector(.2, -.2, .2), Color(1, .5, 0, 2)))
        objects.append(Sphere(.05, Vector(-.27, 0, .1), Color(0, 0, 1, 1)))
        objects.append(Sphere(.05, Vector(-.17, .17, .2), Color(1, 0, 1, 1)))
        objects.append(Sphere(.05, Vector(.0, .25, .15), Color(1, 0, 0, 1)))


        # objects.append(Sphere(.1, Vector(0, -.2, 0), Color(.1,.1,.1, 2)))
        # objects.append(Sphere(.1, Vector(.15, .1, .05), Color(0, 1, 0, 1)))
        # objects.append(Sphere(.1, Vector(-.15, .1, .05), Color(0, 0, 1, 1)))

        # objects.append(Triangle(Vector(.3, -.35, -.2).negative(), Vector(.2, .25, -.1).negative(), Vector(-.3, -.3, .2).negative(), Color(0,0,1, 1)))
        # objects.append(Triangle(Vector(.2, -.1, .1), Vector(.2, .5, .2), Vector(.2, -.1, -.35), Color(1, 1, 0, 1)))

        f = open("extra.ppm", "w")
        f.write("P3\n" + str(width) + "\n" + str(height) + "\n255\n")
        checkIntersects = []
        for i in range(width):
            for j in range(height):
                xamnt = (i + 0.5)/width
                yamnt = (((height - j) + 0.5)/height)

                rayDirection = camDir.add(camRight.multiply(xamnt-0.5).add(camDown.multiply(yamnt-0.5))).normalize()

                newRay = Ray(self.camPosition, rayDirection)

                intersections = []

                for obj in objects:
                    newInter = obj.intersect(newRay)
                    intersections.append(newInter)
                    if newInter != -1:
                        checkIntersects.append(newInter)
                bestIndex = self.calcClosestObject(intersections)
                if bestIndex == -1:
                    pixels.append(bgColor)
                else:
                    if (intersections[bestIndex] > accuracy):
                        intersectPos = camPosition.add(rayDirection.multiply(intersections[bestIndex]))
                        intersectDir = rayDirection
                        intersectColor = self.getColorAt(intersectPos, intersectDir, objects, bestIndex, accuracy, ambientLight, light, 0, 36)

                        pixels.append(intersectColor)

            self.rays.append(newRay)
        newRay.printPoint()
        for i in range(len(pixels)):
            f.write(pixels[i].toString())

if __name__ == '__main__':
    rayTracer = RayTracer()
    rayTracer.main()