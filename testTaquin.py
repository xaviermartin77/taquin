# Python program to read 
# image using PIL module 
  
# importing PIL 
import math 
from PIL import Image, ImageDraw
import pygame
from pygame.locals import *
import random
import os

MAX_WIDTH = 1500
MAX_HEIGHT = 1000
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)


class ImagesGrid:
        def __init__(self):
                self.imageList = getAllImages(ecran)
                self.firstListIndex = 0

class GameGrid:
        def __init__(self):
                self.imageList = getAllImages(ecran)
                self.firstListIndex = 0

'''

# code mort, à relire
def gridImage(imageName, grid_width, grid_height, targetName):
        img = Image.open(imageName)
        w, h = img.size
  
        img1 = ImageDraw.Draw(img)
        for x in range(1, grid_width):
                img1.line([((x)*w/grid_width, 0), ((x)*w/grid_width, h)], fill ="red", width = 0)
        for y in range(1, grid_height):
                img1.line([(0, (y)*h/grid_height), w, ((y)*h/grid_height)], fill ="red", width = 0)
        img.save(targetName)
        # img.show()


def tilesFromImage(imageName, grid_width, grid_height):
        img = Image.open(imageName)
        w, h = img.size
        for x in range(grid_width):
                for y in range(grid_height):
                        fileName = os.path.splitext(imageName)[0] + '_' + str(x) + '_' + str(y) + '.jpg'
                        img.crop((x*w/grid_width, y*h/grid_height, (x+1)*w/grid_width, (y+1)*h/grid_height)).save(fileName)
'''

# récupérer les images, à garder en static, maybe mettre un fichier de config, maybe faire un tableau d'id plutôt que d'images
def getAllImages(screen):
        fileExist = True
        fileCount = 1
        fileList = []
        while fileExist:
                fileName = 'images/image' + str(fileCount) + '.jpg'
                if os.path.isfile(fileName):
                        tempImage = pygame.image.load(fileName)
                        tempImage = pygame.transform.scale(tempImage, (int(screen.get_width()/4), int(screen.get_height()/4)))
                        fileList.append(tempImage)
                        fileCount = fileCount + 1
                else:
                        fileExist = False
        return fileList


# static, calcule la taille de l'image par rapport à l'écran
def getImageSize(imageWidth, imageHeight, grid_width, grid_height):
        screen_width = min(MAX_WIDTH - 100, imageWidth)
        screen_height = screen_width * imageHeight / imageWidth
        if screen_height > MAX_HEIGHT:
                screen_height = min(MAX_HEIGHT, imageHeight)
                screen_width = screen_height * imageWidth / imageHeight
        adjusted_screen_width = int(screen_width) - int(screen_width)%grid_width
        adjusted_screen_height = int(screen_height) - int(screen_height)%grid_height
        return int(adjusted_screen_width), int(adjusted_screen_height)

# method UI, affiche l'image de la tuile sur l'écran (screen), attention au move (utilisé pour le mouvement des tuiles)
def displayTileImage(screen, image, tileWidth, tileHeight, tilePositionX, tilePositionY, tileIndexX, tileIndexY, text = '', move = (0,0)):
        tileCoordinateX = tileWidth*tileIndexX + move[0]
        tileCoordinateY = tileHeight*tileIndexY + move[1]
        tileLocationX = tileWidth*tilePositionX
        tileLocationY = tileHeight*tilePositionY
        screen.blit(image, (tileCoordinateX, tileCoordinateY), (tileLocationX, tileLocationY, tileWidth, tileHeight))

        if (text != ''):
                ariaFont = pygame.font.SysFont('arial', 50, False, False)
                textSurface = ariaFont.render(text, True, (255, 0, 0))
                textRect = textSurface.get_rect()
                textRect.center = (tileCoordinateX + tileWidth/2, tileCoordinateY + tileHeight/2)
                screen.blit(textSurface, textRect)
        moveStep = tileWidth/10 if move[0] !=0 else tileHeight/10
        if move[0] + move[1] > 0:
                return move[0] + move[1] + moveStep
        if move[0] + move[1] < 0:
                return move[0] + move[1] - moveStep
        return 0

# static, génère un array random mais solvable
def getRandomArray(width, height):
        size = width * height
        array = list(range(size))
        solvable = False
        while not solvable:
                random.shuffle(array)
                testArray = list(range(size))
                count = 0
                for i in range(size):
                        testArray[i] = array[i]
                        if testArray[i] == size-1:
                                x,y = getPositionFromIndex(i, width)
                                count = count + width + height - x - y
                for i in range(size):
                        if testArray[i] != i:
                                for j in range(i,size):
                                        if testArray[j] == i:
                                                testArray[j] = testArray[i]
                                                testArray[i] = i
                                                count = count + 1
                solvable = (count%2 == 0)
        return array

# static, récupère la position d'une tuile à partir de son index (utils)
def getPositionFromIndex(index, width):
        return index % width, index // width

# method UI, affiche toutes les tuiles, sur méthode de displayTileImage (progress -> move)
def displayAllTiles(screen, image, array, tileWidth, tileHeight, grid_width, grid_height, showText, currentMovement):
        text = ''
        progress, tile, target = currentMovement
        move = (0,0)
        newProgress = 0
        for x in range(grid_width):
                for y in range(grid_height):
                        i,j = getPositionFromIndex(array[y*grid_width + x], grid_width)
                        if i == grid_width-1 and j == grid_height-1 and not solved(array):
                                continue
                        if showText:
                                text = str(j*grid_width + i + 1)
                        if progress != 0 and y*grid_width + x == tile:
                                if tile == target-1 or tile == target+1:
                                        move = (progress, 0)
                                if tile == target-grid_width or tile == target+grid_width:
                                        move = (0, progress)
                                newProgress = displayTileImage(screen, image, tileWidth, tileHeight, i, j, x, y, text, move)
                        else:
                                displayTileImage(screen, image, tileWidth, tileHeight, i, j, x, y, text)
        return newProgress

# method tapHandler, récupère l'index d'une tile cliquée (ou -1 si on ne trouve rien)
def getTileCoordinate(x, y, tileWidth, tileHeight, grid_width, grid_height):
        for i in range(grid_width):
                for j in range(grid_height):
                        if x >= tileWidth*i and x < tileWidth*(i+1) and y >= tileHeight*j and y < tileHeight*(j+1):
                                return j*grid_width + i
        return -1
# method liée à la grid, détermine si la tuile peut bouger (et renvoie l'index cible le mvt est possible)
def canMoveTo(array, index, grid_width, grid_height):
        if index == -1:
                return -1
        if array[index] == (grid_width * grid_height) -1:
                return -1
        i,j = getPositionFromIndex(index, grid_width)
        if i>0 and array[index-1] == (grid_width * grid_height) -1:
                return index-1
        if i<grid_width-1 and array[index+1] == (grid_width * grid_height) -1:
                return index+1
        if j>0 and array[index-grid_width] == (grid_width * grid_height) -1:
                return index-grid_width
        if j<grid_height-1 and array[index+grid_width] == (grid_width * grid_height) -1:
                return index+grid_width
        return -1

# method liée à la grid, détermine si la grid est résolue
def solved(array):
        return all(array[i] <= array[i+1] for i in range(len(array)-1))

# method UI, montre l'indice (l'image complète)
def showHint(screen, image):
        screen.blit(image, (0,0))

# method animationHandler, détermine si le mouvement de la tuile est terminé
def isMovementOver(move, tileWidth, tileHeight, grid_width):
        progress, tile, target = move
        if tile == target-1 and progress >= tileWidth:
                return True
        if tile == target+1 and progress <= -tileWidth:
                return True
        if tile == target-grid_width and progress >= tileHeight:
                return True
        if tile == target+grid_width and progress <= -tileHeight:
                return True
        return False

# method UI, affiche l'interface pendant le jeu (indice, redémarrer, score, temps, couleur du fond)
# to add : back, solve, shortcuts
def display_game_interface(screen, showing_score, score, showing_time, time, solved):
        ariaFont = pygame.font.SysFont('arial', 20, False, False)

        firstText = 'Menu' if solved else 'Hint'
        textSurface = ariaFont.render(firstText, True, black)
        textRect = textSurface.get_rect()
        textRect.center = (screen.get_width() - 50, screen.get_height()/10)
        screen.blit(textSurface, textRect)

        pygame.draw.line(screen, black, (screen.get_width() - 100, screen.get_height()/5), (screen.get_width(), screen.get_height()/5))

        secondText = 'Restart' if solved else 'Figures'
        textSurface = ariaFont.render(secondText, True, black)
        textRect = textSurface.get_rect()
        textRect.center = (screen.get_width() - 50, 3*screen.get_height()/10)
        screen.blit(textSurface, textRect)

        pygame.draw.line(screen, black, (screen.get_width() - 100, 2*screen.get_height()/5), (screen.get_width(), 2*screen.get_height()/5))

        scoreText = 'Score'
        if showing_score:
                scoreText = str(score)
        textSurface = ariaFont.render(scoreText, True, black)
        textRect = textSurface.get_rect()
        textRect.center = (screen.get_width() - 50, 5*screen.get_height()/10)
        screen.blit(textSurface, textRect)

        pygame.draw.line(screen, black, (screen.get_width() - 100, 3*screen.get_height()/5), (screen.get_width(), 3*screen.get_height()/5))

        timeText = 'Time'
        if showing_time:
                timeText = str(time)
        textSurface = ariaFont.render(timeText, True, black)
        textRect = textSurface.get_rect()
        textRect.center = (screen.get_width() - 50, 7*screen.get_height()/10)
        screen.blit(textSurface, textRect)

        pygame.draw.line(screen, black, (screen.get_width() - 100, 4*screen.get_height()/5-1), (screen.get_width(), 4*screen.get_height()/5-1))
        
        screen.fill(white, (screen.get_width()-100, 4*screen.get_height()/5, 100, screen.get_height()/25))
        screen.fill(black, (screen.get_width()-100, 21*screen.get_height()/25, 100, screen.get_height()/25))
        screen.fill(red, (screen.get_width()-100, 22*screen.get_height()/25, 100, screen.get_height()/25))
        screen.fill(blue, (screen.get_width()-100, 23*screen.get_height()/25, 100, screen.get_height()/25))
        screen.fill(green, (screen.get_width()-100, 24*screen.get_height()/25, 100, screen.get_height()/25))


# method UI, affiche l'interface avant le jeu (image sélectionnée, nombre de tuiles longueur et largeut, démarrer)
# to add : hint, stats
def display_start_interface(screen, image_index, grid_width, grid_height):
        
        index_x = image_index % 3
        index_y = image_index // 3
        pygame.draw.line(screen, red, (index_x*screen.get_width()/4, index_y*screen.get_height()/4), ((index_x+1)*screen.get_width()/4, index_y*screen.get_height()/4))
        pygame.draw.line(screen, red, (index_x*screen.get_width()/4, (index_y+1)*screen.get_height()/4), ((index_x+1)*screen.get_width()/4, (index_y+1)*screen.get_height()/4))
        pygame.draw.line(screen, red, (index_x*screen.get_width()/4, index_y*screen.get_height()/4), (index_x*screen.get_width()/4, (index_y+1)*screen.get_height()/4))
        pygame.draw.line(screen, red, ((index_x+1)*screen.get_width()/4, index_y*screen.get_height()/4), ((index_x+1)*screen.get_width()/4, (index_y+1)*screen.get_height()/4))
        
        ariaFont = pygame.font.SysFont('arial', 50, False, False)
        
        textSurface = ariaFont.render('Width', True, black)
        textRect = textSurface.get_rect()
        textRect.center = (screen.get_width()*7/8, screen.get_height()/6 - 40)
        screen.blit(textSurface, textRect)
        
        textSurface = ariaFont.render(str(grid_width), True, black)
        textRect = textSurface.get_rect()
        textRect.center = (screen.get_width()*7/8, screen.get_height()/6 + 40)
        screen.blit(textSurface, textRect)

        minusTextWidth = '-' if grid_width > 2 else ''
        textSurface = ariaFont.render(minusTextWidth, True, black)
        textRect = textSurface.get_rect()
        textRect.center = (screen.get_width()*13/16, screen.get_height()/6 + 40)
        screen.blit(textSurface, textRect)

        plusTextWidth = '+' if grid_width < 20 else ''
        textSurface = ariaFont.render(plusTextWidth, True, black)
        textRect = textSurface.get_rect()
        textRect.center = (screen.get_width()*15/16, screen.get_height()/6 + 40)
        screen.blit(textSurface, textRect)
        
        pygame.draw.line(screen, black, (screen.get_width()*3/4, screen.get_height()/3), (screen.get_width(), screen.get_height()/3))
        
        textSurface = ariaFont.render('Height', True, black)
        textRect = textSurface.get_rect()
        textRect.center = (screen.get_width()*7/8, 3*screen.get_height()/6 - 40)
        screen.blit(textSurface, textRect)
        
        textSurface = ariaFont.render(str(grid_height), True, black)
        textRect = textSurface.get_rect()
        textRect.center = (screen.get_width()*7/8, 3*screen.get_height()/6 + 40)
        screen.blit(textSurface, textRect)

        minusTextHeight = '-' if grid_height > 2 else ''
        textSurface = ariaFont.render(minusTextHeight, True, black)
        textRect = textSurface.get_rect()
        textRect.center = (screen.get_width()*13/16, 3*screen.get_height()/6 + 40)
        screen.blit(textSurface, textRect)

        plusTextHeight = '+' if grid_height < 20 else ''
        textSurface = ariaFont.render(plusTextHeight, True, black)
        textRect = textSurface.get_rect()
        textRect.center = (screen.get_width()*15/16, 3*screen.get_height()/6 + 40)
        screen.blit(textSurface, textRect)

        pygame.draw.line(screen, black, (screen.get_width()*3/4, 2*screen.get_height()/3), (screen.get_width(), 2*screen.get_height()/3))

        textSurface = ariaFont.render('Start', True, black)
        textRect = textSurface.get_rect()
        textRect.center = (screen.get_width()*7/8, 5*screen.get_height()/6)
        screen.blit(textSurface, textRect)

# method tapHandler, liée à la grid, renvoie la tuile vide et la tuile à bouger
def autoMoveTarget(currentArray, direction, grid_width, grid_height):

        '''
        (autoTile, autoTargetTile) = autoMoveTarget(currentArray, 2, grid_width, grid_height)
                if autoTargetTile != -1 and not solved(currentArray) :
                        if start_ticks == 0:
                                start_ticks = pygame.time.get_ticks()
                        move_count = move_count + 1
                        firstProgress = 1 if autoTile < autoTargetTile else -1
                        currentMovement = (firstProgress, autoTile, autoTargetTile)
        '''
        
        target_tile = -1
        for i in range(len(currentArray)):
                if currentArray[i] == len(currentArray)-1:
                        target_tile = i
                        break
        
        if target_tile == -1:
                return (-1,-1)
        
        i,j = getPositionFromIndex(target_tile, grid_width)
        
        if i>0 and direction == 0:
                # move left
                return ((i - 1) + j*grid_width, i + j*grid_width)
        if i<grid_width-1 and direction == 1:
                # move right
                return ((i + 1) + j*grid_width, i + j*grid_width)
        if j>0 and direction == 2:
                # move down
                return (i + (j-1)*grid_width, i + j*grid_width)
        if j<grid_height-1 and direction == 3:
                # move up
                return (i + (j+1)*grid_width, i + j*grid_width)
        #print('tried move ' + str(direction))
        return (-1, -1)

'''
# solver, à voir plus tard

def getNextMove(currentArray, grid_width, grid_height):
        if solved(currentArray):
                return(-1,-1)
        solvedColumnCount = 0
        solvedLineCount = 0
        indexToSolve = -1
        for i in range(len(currentArray)):
                if currentArray[i] == i:
                        solvedColumnCount = solvedColumnCount + 1
                        if solvedColumnCount == grid_width:
                                solvedColumnCount = 0
                                solvedLineCount = solvedLineCount + 1
                else:
                        indexToSolve = i
                        break
        if grid_height - solvedLineCount < 3:
                solvedColumnCount = 0
                for j in range(grid_width):
                        firstIndex = grid_width*(grid_height-2) + j
                        secondIndex = grid_width*(grid_height-1) + j
                        if currentArray[firstIndex] == firstIndex and currentArray[secondIndex] == secondIndex:
                                solvedColumnCount = solvedColumnCount + 1
                        else:
                                break
                if grid_width - solvedColumnCount < 3:
                        firstIndex = grid_width*(grid_height-1) - 2
                        return solveSquare(currentArray, firstIndex, grid_width, grid_height)
                else:
                        return solveDoubleHorizontal(currentArray, solvedColumnCount, grid_width, grid_height)
        else:
                if grid_width - solvedColumnCount < 3:
                        return solveDoubleVertical(currentArray, solvedLineCount, grid_width, grid_height)
                else:
                        return solveGeneral(currentArray, indexToSolve, grid_width, grid_height)
        return(-1,-1)


def solveSquare(currentArray, firstIndex, grid_width, grid_height):
        lastIndex = firstIndex + grid_width + 1
        squareArray = [currentArray[firstIndex], currentArray[firstIndex + 1], currentArray[firstIndex + grid_width], currentArray[firstIndex + grid_width + 1]]
        if squareArray[0] ==  firstIndex:
                if squareArray[1] == lastIndex:
                        return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, False)
                else:
                        return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, True)
        if squareArray[1] ==  firstIndex:
                return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, False)
        if squareArray[2] ==  firstIndex:
                return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, True)
        if squareArray[3] ==  firstIndex:
                if squareArray[1] == lastIndex:
                        return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, False)
                else:
                        return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, True)
        return(-1,-1)

def solveDoubleHorizontal(currentArray, target_column, grid_width, grid_height):
        up_target_index = (grid_height - 2) * grid_width + target_column
        down_target_index = (grid_height - 1) * grid_width + target_column
        
        blank_index = -1
        up_index = -1
        down_index = -1
        for i in range(len(currentArray)):
                if currentArray[i] == len(currentArray)-1:
                        blank_index = i
                if currentArray[i] == up_target_index:
                        up_index = i
                if currentArray[i] == down_target_index:
                        down_index = i
                if blank_index != -1 and up_index != -1 and down_index != -1:
                        break
        if blank_index == -1 or up_index == -1 or down_index == -1 :
                return (-1,-1)

        blank_x, blank_y = getPositionFromIndex(blank_index, grid_width)
        up_x, up_y = getPositionFromIndex(up_index, grid_width)
        down_x, down_y = getPositionFromIndex(down_index, grid_width)
        target_x = target_column
        target_up_y = grid_height - 2
        target_down_y = grid_height - 1
        
        if (blank_x < target_x + 3) and (up_x < target_x + 3) and (down_x < target_x + 3):
                if up_x == target_x and down_x == target_x:
                        return autoMoveTarget(currentArray, 0, grid_width, grid_height)
                if (up_x == target_x) or (down_x == target_x):
                        if blank_x == target_x:
                                if up_x == target_x + 1 or  down_x == target_x + 1:
                                        if (up_x == target_x and up_y > blank_y) or (down_x == target_x and down_y < blank_y):
                                                orientation = 2 if blank_y == grid_height - 1 else 3
                                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                                        else:
                                                return autoMoveTarget(currentArray, 1, grid_width, grid_height)
                                else:
                                        if (up_x == target_x and up_y < blank_y) or (down_x == target_x and down_y > blank_y):
                                                orientation = 2 if blank_y == grid_height - 1 else 3
                                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                                        else:
                                                return autoMoveTarget(currentArray, 1, grid_width, grid_height)
                        if (up_y == target_up_y and up_x == target_x) or (down_y == target_down_y and down_x == target_x):
                                if blank_x == target_x + 1 and ((up_x == target_x and blank_y != up_y and (up_y != down_y or down_x != up_x + 1)) or (down_x == target_x and blank_y != down_y and (up_y != down_y or up_x != down_x + 1))):
                                        return autoMoveTarget(currentArray, 0, grid_width, grid_height)
                                else:
                                        #TODO : find good rotate orientation
                                        firstIndex = up_target_index + 1
                                        lastIndex = firstIndex + grid_width + 1
                                        return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, True)
                        else:
                                if blank_x == target_x + 1 and ((up_y == target_up_y and up_x == target_x + 1) or (down_y == target_down_y and down_x == target_x + 1)):
                                        return autoMoveTarget(currentArray, 0, grid_width, grid_height)
                                else:
                                        #TODO : find good rotate orientation
                                        firstIndex = up_target_index + 1
                                        lastIndex = firstIndex + grid_width + 1
                                        return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, True)
                else:
                        if blank_x == target_x and up_x == down_x:
                                return autoMoveTarget(currentArray, 1, grid_width, grid_height)
                        if blank_x < target_x + 2 and ((up_x == target_x + 2 and down_x < target_x + 2) or (up_x < target_x + 2 and down_x == target_x + 2)):
                                orientation = True if up_x < target_x + 2 else False
                                firstIndex = up_target_index
                                lastIndex = firstIndex + grid_width + 1
                                return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, orientation)
                        else:
                                #TODO : find good rotate orientation
                                firstIndex = up_target_index + 1
                                lastIndex = firstIndex + grid_width + 1
                                return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, True)

        
        if (blank_x < up_x and blank_x > down_x) or (blank_x > up_x and blank_x < down_x) or (blank_x < up_x and blank_x < down_x):
                if ((blank_x == up_x - 1 and blank_y != up_y) or (blank_x == down_x - 1 and blank_y != down_y)) and up_x != down_x:
                        orientation = 2 if blank_y == grid_height - 1 else 3
                        return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                return autoMoveTarget(currentArray, 1, grid_width, grid_height)
        
        if blank_x > up_x and blank_x > down_x:
                if ((blank_y == up_y and blank_x == up_x + 1) or (blank_y == down_y and blank_x == down_x + 1)) and up_x != down_x:
                        orientation = 2 if blank_y == grid_height - 1 else 3
                        return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                else:
                        return autoMoveTarget(currentArray, 0, grid_width, grid_height)
                
        if blank_x == up_x or blank_x == down_x:
                if blank_x < up_x or blank_x < down_x:
                        if (blank_x == up_x and up_y == target_up_y) or (blank_x == down_x and down_y == target_down_y):
                                orientation = 2 if blank_y == grid_height - 1 else 3
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                        else:
                                if (up_x == blank_x + 1) or (down_x == blank_x + 1):
                                        return autoMoveTarget(currentArray, 0, grid_width, grid_height)
                                else:
                                        return autoMoveTarget(currentArray, 1, grid_width, grid_height)
                else:
                        if up_y != down_y:
                                orientation = 2 if blank_y == grid_height - 1 else 3
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                        else:
                                return autoMoveTarget(currentArray, 0, grid_width, grid_height)
                                
                                
        
        return(-1,-1)

def solveDoubleVertical(currentArray, target_line, grid_width, grid_height):
        left_target_index = (target_line + 1) * grid_width - 2
        right_target_index = (target_line + 1) * grid_width - 1

        blank_index = -1
        left_index = -1
        right_index = -1
        for i in range(len(currentArray)):
                if currentArray[i] == len(currentArray)-1:
                        blank_index = i
                if currentArray[i] == left_target_index:
                        left_index = i
                if currentArray[i] == right_target_index:
                        right_index = i
                if blank_index != -1 and left_index != -1 and right_index != -1:
                        break
        if blank_index == -1 or left_index == -1 or right_index == -1 :
                return (-1,-1)

        blank_x, blank_y = getPositionFromIndex(blank_index, grid_width)
        left_x, left_y = getPositionFromIndex(left_index, grid_width)
        right_x, right_y = getPositionFromIndex(right_index, grid_width)
        target_y = target_line
        target_left_x = grid_width - 2
        target_right_x = grid_width - 1

        # cas à gérer : left ou right ou blank pas encore dans les colonnes
        if blank_x < target_left_x or left_x < target_left_x or right_x < target_left_x:
                # left et right dans la bonne colonne mais pas blank
                if (left_x >= target_left_x and right_x >= target_left_x):
                        if blank_y == left_y or blank_y == right_y:
                                # TODO : handle special case 3 line missing, left and right blocking blank
                                if blank_y  == target_y + 1:
                                        return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                                if blank_y  == grid_height - 1:
                                        return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                                if left_y == target_y + 1 or right_y == target_y + 1:
                                        return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                                else:
                                        return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                        else:
                                return autoMoveTarget(currentArray, 1, grid_width, grid_height)
                # blank à droite de left et right
                if left_x < blank_x and right_x < blank_x:
                        # blank parmi les deux cases target, aller vers le bas
                        if blank_y == target_y:
                                return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                        # aller vers la droite, sauf si les deux cases sur la même colonne juste à gauche, alors aller à la hauteur du plus haut, puis aller vers la droite
                        else:
                                print('cas particulier')
                                # return autoMoveTarget(currentArray, 0, grid_width, grid_height)
                # blank à gauche de left et right
                if left_x > blank_x and right_x > blank_x:
                        # left ou right dans la colonne juste à droite, ne pas aller vers la gauche, aller vers le haut ou le bas selon les cas
                        if (blank_y == left_y and left_x == blank_x + 1) or (blank_y == right_y and right_x == blank_x + 1):
                                print('cas particulier')
                        # aller vers la gauche
                        else:
                                return autoMoveTarget(currentArray, 1, grid_width, grid_height)
                # blank entre left et right, se mettre au niveau de la plus à gauche puis aller vers la droite
                if (left_x < blank_x and right_x > blank_x) or (left_x > blank_x and right_x < blank_x):
                        print('cas particulier')
                        #return autoMoveTarget(currentArray, 0, grid_width, grid_height)
                # blank sur la colonne de left ou de right
                # à gérer : autre case à gauche -> aller vers la gauche (aller chercher l'autre cas, prioritaire)
                # à gérer : autre case à droite -> bouger la case verticalement vers l'autre (ou le plus haut possible si case tout en haut)
                # à gérer : autre case sur la même colonne -> si case la plus basse en dessous, monter, si blank en dessous des deux cases adjacentes, aller vers la gauche, sinon aller vers la droite (pour se décaler et continuer la montée)
                        
                # cas blank à gauche des deux : aller vers la droite sauf si un des deux sur le chemin (cf les deux déjà dans la colonne ?)
                # cas blank à droite des deux : aller vers la gauche, sauf si sur la ligne en cours de solve
                # cas entre les deux : aller vers la droite (attention cas particuliers ?)
                # cas meme colonne que celui de droite
                # cas meme colonne que celui de gauche
                # stratégie : mettre les 2 sur la meme ligne en gérant la partie gauche d'abord, gérer les cas particuliers 'tout à gauche' et 'sur la meme colonne'

                # si plus d'une colonne d'écart : décaler le plus à gauche vers la droite (à développer)
                # si meme colonne : passer par le haut ou le bas pour décaller celui du haut vers la droite (attention : cas particulier 3 lignes à solve)
                # si une colonne d'écart : monter le plus en bas (passer par la droite ou la gauche)
                # si une colonne d'écart, les 2 sur la meme ligne : décaller l'ensemble vers la droite

        # deux dernières colonnes uniquement, blank ou left ou right pas encore dans un bloc de 6
        if (blank_y < target_y + 3) and (left_y < target_y + 3) and (right_y < target_y + 3):
                if left_y == target_y and right_y == target_y:
                        return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                if (left_y == target_y) or (right_y == target_y):
                        if blank_y == target_y:
                                if right_y == target_y + 1 or  left_y == target_y + 1:
                                        if (left_y == target_y and left_x > blank_x) or (right_y == target_y and right_x < blank_x):
                                                orientation = 0 if blank_x == grid_width - 1 else 1
                                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                                        else:
                                                return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                                else:
                                        if (left_y == target_y and left_x < blank_x) or (right_y == target_y and right_x > blank_x):
                                                orientation = 0 if blank_x == grid_width - 1 else 1
                                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                                        else:
                                                return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                        if (left_x == target_left_x and left_y == target_y) or (right_x == target_right_x and right_y == target_y):
                                if blank_y == target_y + 1 and ((left_y == target_y and blank_x != left_x and (right_x != left_x or right_y != left_y + 1)) or (right_y == target_y and blank_x != right_x and (right_x != left_x or left_y != right_y + 1))):
                                        return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                                else:
                                        #TODO : find good rotate orientation
                                        firstIndex = left_target_index + grid_width
                                        lastIndex = firstIndex + grid_width + 1
                                        return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, True)
                        else:
                                if blank_y == target_y + 1 and ((left_x == target_left_x and left_y == target_y + 1) or (right_x == target_right_x and right_y == target_y + 1)):
                                        return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                                else:
                                        #TODO : find good rotate orientation
                                        firstIndex = left_target_index + grid_width
                                        lastIndex = firstIndex + grid_width + 1
                                        return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, True)
                else:
                        if blank_y == target_y and left_y == right_y:
                                return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                        if blank_y < target_y + 2 and ((left_y == target_y + 2 and right_y < target_y + 2) or (left_y < target_y + 2 and right_y == target_y + 2)):
                                orientation = True if right_y < target_y + 2 else False
                                firstIndex = left_target_index
                                lastIndex = firstIndex + grid_width + 1
                                return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, orientation)
                        else:
                                #TODO : find good rotate orientation
                                firstIndex = left_target_index + grid_width
                                lastIndex = firstIndex + grid_width + 1
                                return rotate(currentArray, firstIndex, lastIndex, grid_width, grid_height, True)
        # bloc de 6 (les 3 paragraphes)       
        if (blank_y < left_y and blank_y > right_y) or (blank_y > left_y and blank_y < right_y) or (blank_y < left_y and blank_y < right_y):
                if ((blank_y == left_y - 1 and blank_x != left_x) or (blank_y == right_y - 1 and blank_x != right_x)) and left_y != right_y:
                        orientation = 0 if blank_x == grid_width - 1 else 1
                        return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                return autoMoveTarget(currentArray, 3, grid_width, grid_height)
        
        if blank_y > left_y and blank_y > right_y:
                if ((blank_x == right_x and blank_y == right_y + 1) or (blank_x == left_x and blank_y == left_y + 1)) and left_y != right_y:
                        orientation = 0 if blank_x == grid_width - 1 else 1
                        return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                else:
                        return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                
        if blank_y == left_y or blank_y == right_y:
                if blank_y < left_y or blank_y < right_y:
                        if (blank_y == left_y and left_x == target_left_x) or (blank_y == left_y and left_x == target_left_x):
                                orientation = 0 if blank_x == grid_width - 1 else 1
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                        else:
                                if (left_y == blank_y + 1) or (right_y == blank_y + 1):
                                        return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                                else:
                                        return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                else:
                        if left_x != right_x:
                                orientation = 0 if blank_x == grid_width - 1 else 1
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                        else:
                                return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                                
                                
        
        return(-1,-1)

def solveGeneral(currentArray, target_index, grid_width, grid_height):
        blank_index = -1
        tile_index = -1
        for i in range(len(currentArray)):
                if currentArray[i] == len(currentArray)-1:
                        blank_index = i
                if currentArray[i] == target_index:
                        tile_index = i
                if blank_index != -1 and tile_index != -1:
                        break
        if blank_index == -1 or tile_index == -1:
                return (-1,-1)
        
        blank_x, blank_y = getPositionFromIndex(blank_index, grid_width)
        target_x, target_y = getPositionFromIndex(target_index, grid_width)
        tile_x, tile_y = getPositionFromIndex(tile_index, grid_width)
        
        if tile_x == target_x:
                if blank_y < tile_y:
                        if blank_x == tile_x:
                                return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                        else:
                                orientation = 0 if blank_x > tile_x else 1
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                if blank_y == tile_y:
                        orientation = 3 if (blank_x < tile_x and tile_y == target_y + 1) else 2
                        return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                if blank_y > tile_y:
                        if blank_x == tile_x:
                                return autoMoveTarget(currentArray, 1, grid_width, grid_height)
                        if blank_x > tile_x:
                                return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                        if blank_x < tile_x:
                                orientation = 3 if tile_y > target_y + 1 else 1
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
        else:
                if (blank_x < tile_x and target_x <= blank_x) or (blank_x > tile_x and target_x >= blank_x):
                        if blank_y == tile_y:
                                orientation = 1 if blank_x < tile_x else 0
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                        else:
                                orientation = 2 if blank_y > tile_y else 3
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                if blank_x == tile_x:
                        if blank_y < tile_y:
                                return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                        else:
                                orientation = 1 if target_x > tile_x else 0
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                if (blank_x > tile_x and target_x <= blank_x) or (blank_x < tile_x and target_x >= blank_x):
                        if blank_y == tile_y:
                                orientation = 2 if tile_y > target_y + 1 else 3
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
                        else:
                                orientation = 0 if blank_x > tile_x else 1
                                return autoMoveTarget(currentArray, orientation, grid_width, grid_height)
        return(-1,-1)


def rotate(currentArray, start_index, end_index, grid_width, grid_height, rotate_chrono):
        blank_index = -1
        for i in range(len(currentArray)):
                if currentArray[i] == len(currentArray)-1:
                        blank_index = i
                        break
        
        if blank_index == -1:
                return (-1,-1)
        
        blank_x, blank_y = getPositionFromIndex(blank_index, grid_width)
        start_x, start_y = getPositionFromIndex(start_index, grid_width)
        end_x, end_y = getPositionFromIndex(end_index, grid_width)
        
        if blank_x >= start_x and blank_x <= end_x and blank_y == start_y:
                if rotate_chrono and blank_x != start_x:
                        return autoMoveTarget(currentArray, 0, grid_width, grid_height)
                if (not rotate_chrono) and blank_x != end_x:
                        return autoMoveTarget(currentArray, 1, grid_width, grid_height)
        if blank_x >= start_x and blank_x <= end_x and blank_y == end_y:
                if rotate_chrono and blank_x != end_x:
                        return autoMoveTarget(currentArray, 1, grid_width, grid_height)
                if (not rotate_chrono) and blank_x != start_x:
                        return autoMoveTarget(currentArray, 0, grid_width, grid_height)
        if blank_y >= start_y and blank_y <= end_y and blank_x == start_x:
                if rotate_chrono and blank_y != end_y:
                        return autoMoveTarget(currentArray, 3, grid_width, grid_height)
                if (not rotate_chrono) and blank_y != start_y:
                        return autoMoveTarget(currentArray, 2, grid_width, grid_height)
        if blank_y >= start_y and blank_y <= end_y and blank_x == end_x:
                if rotate_chrono and blank_y != start_y:
                        return autoMoveTarget(currentArray, 2, grid_width, grid_height)
                if (not rotate_chrono) and blank_y != end_y:
                        return autoMoveTarget(currentArray, 3, grid_width, grid_height)
        return(-1,-1)


# algo brute force

def getKeyFromArray(array):
        strings = [str(integer) for integer in array]
        string = "".join(strings)
        return int(string)

def solveBruteForce(currentArray, grid_width, grid_height):
        size = grid_width * grid_height
        solvedArray = list(range(size))

        #print(getKeyFromArray(currentArray))
        shortest_ways = {}
        shortest_ways[getKeyFromArray(solvedArray)] = []
        current_list = [solvedArray]
        next_list = []

        while len(shortest_ways) < math.factorial(size)/2:
                next_list = []
                for array in current_list:
                        for i in range(4):
                                (tile, targetTile) = autoMoveTarget(array, i, grid_width, grid_height)
                                if targetTile == -1:
                                        continue
                                newArray = list(range(size))
                                for j in range(size):
                                        newArray[j] = array[j]
                                newArray[targetTile] = newArray[tile]
                                newArray[tile] = size - 1
                                if getKeyFromArray(newArray) not in shortest_ways:
                                        if getKeyFromArray(currentArray) == getKeyFromArray(newArray):
                                                return (targetTile, tile)
                                        shortest_way = []
                                        for move in shortest_ways[getKeyFromArray(array)]:
                                                shortest_way.append(move)
                                        shortest_way.append(i)
                                        shortest_ways[getKeyFromArray(newArray)] = shortest_way
                                        next_list.append(newArray)
                current_list = []
                for element in next_list:
                        current_list.append(element)
        #print(shortest_ways[getKeyFromArray(currentArray)])
        return(-1,-1)

'''

# TODO : factorizer les méthodes get UI (tap handler), les variables d'état (dans les classes), ne garder que l'essentiel (ecran, loop)
def playGame():
        pygame.init()
        ecran = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))

        imageList = getAllImages(ecran)
        firstListIndex = 0
        game_started = False
        grid_width = 3
        grid_height = 3
        imageIndex = 0
        
        pygame.display.flip()
        loop = True
        
        while loop:
                start_game = False
                for event in pygame.event.get():
                        if game_started:
                                tile = -1
                                targetTile = -1
                                if currentMovement[0] != 0:
                                        continue
                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                        pos = pygame.mouse.get_pos()
                                        tile = getTileCoordinate(pos[0], pos[1], tileWidth, tileHeight, grid_width, grid_height)
                                        targetTile = canMoveTo(currentArray, tile, grid_width, grid_height)
                                        if pos[0] > ecran.get_width() - 100 and pos[0] < ecran.get_width() and pos[1] > 0 and pos[1] < ecran.get_height()/5:
                                                if solved(currentArray):
                                                        ecran = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
                                                        game_started = False
                                                else:
                                                        showing_hint = True
                                        if pos[0] > ecran.get_width() - 100 and pos[0] < ecran.get_width() and pos[1] > ecran.get_height()/5 and pos[1] < 2*ecran.get_height()/5:
                                                if solved(currentArray):
                                                        start_ticks = 0
                                                        final_time = 0
                                                        seconds = 0
                                                        move_count = 0        
                                                        currentArray = getRandomArray(grid_width, grid_height)
                                                        currentMovement = (0, 0, 0)
                                                else:
                                                        showing_figures = True
                                        if pos[0] > ecran.get_width() - 100 and pos[0] < ecran.get_width() and pos[1] > 2*ecran.get_height()/5 and pos[1] < 3*ecran.get_height()/5:
                                                showing_score = not showing_score
                                        if pos[0] > ecran.get_width() - 100 and pos[0] < ecran.get_width() and pos[1] > 3*ecran.get_height()/5 and pos[1] < 4*ecran.get_height()/5:
                                                showing_time = not showing_time
                                        if pos[0] > ecran.get_width() - 100 and pos[0] < ecran.get_width() and pos[1] > 4*ecran.get_height()/5 and pos[1] < 21*ecran.get_height()/25:
                                                background_color = white
                                        if pos[0] > ecran.get_width() - 100 and pos[0] < ecran.get_width() and pos[1] > 21*ecran.get_height()/25 and pos[1] < 22*ecran.get_height()/25:
                                                background_color = black
                                        if pos[0] > ecran.get_width() - 100 and pos[0] < ecran.get_width() and pos[1] > 22*ecran.get_height()/25 and pos[1] < 23*ecran.get_height()/25:
                                                background_color = red
                                        if pos[0] > ecran.get_width() - 100 and pos[0] < ecran.get_width() and pos[1] > 23*ecran.get_height()/25 and pos[1] < 24*ecran.get_height()/25:
                                                background_color = blue
                                        if pos[0] > ecran.get_width() - 100 and pos[0] < ecran.get_width() and pos[1] > 24*ecran.get_height()/25 and pos[1] < ecran.get_height():
                                                background_color = green
                                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                                        showing_hint = False
                                        showing_figures = False
                                '''if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                                        (tile, targetTile) = getNextMove(currentArray, grid_width, grid_height)
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                                        (tile, targetTile) = solveBruteForce(currentArray, grid_width, grid_height)'''
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                                        (tile, targetTile) = rotate(currentArray, 0, len(currentArray)-1, grid_width, grid_height, True)
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                                        (tile, targetTile) = rotate(currentArray, 0, len(currentArray)-1, grid_width, grid_height, False)
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                                        (tile, targetTile) = autoMoveTarget(currentArray, 0, grid_width, grid_height)
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                                        (tile, targetTile) = autoMoveTarget(currentArray, 1, grid_width, grid_height)
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                                        (tile, targetTile) = autoMoveTarget(currentArray, 2, grid_width, grid_height)
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                                        (tile, targetTile) = autoMoveTarget(currentArray, 3, grid_width, grid_height)
                                        
                                if targetTile != -1 and not solved(currentArray) :
                                        if start_ticks == 0:
                                                start_ticks = pygame.time.get_ticks()
                                        move_count = move_count + 1
                                        firstProgress = 1 if tile < targetTile else -1
                                        currentMovement = (firstProgress, tile, targetTile)

                        else: 
                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                                        firstListIndex = firstListIndex - 3 if firstListIndex - 3 >= 0 else 0
                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                                        firstListIndex = firstListIndex + 3 if firstListIndex + 12 < len(imageList) else firstListIndex
                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                        pos = pygame.mouse.get_pos()
                                        if pos[0] > 0 and pos[0] < 3*ecran.get_width()/4 and pos[1] > 0 and pos[1] < ecran.get_height():
                                                index_x = int(pos[0]) // int(ecran.get_width()/4)
                                                index_y = int(pos[1]) // int(ecran.get_height()/4)
                                                if index_x + 3 * index_y + firstListIndex < len(imageList):
                                                        imageIndex = index_x + 3 * index_y + firstListIndex
                                        if pos[0] > 3*ecran.get_width()/4 and pos[0] < 7*ecran.get_width()/8 and pos[1] > 0 and pos[1] < ecran.get_height()/3:
                                                grid_width = grid_width - 1 if grid_width > 2 else grid_width
                                        if pos[0] > 7*ecran.get_width()/8 and pos[0] < ecran.get_width() and pos[1] > 0 and pos[1] < ecran.get_height()/3:
                                                grid_width = grid_width + 1 if grid_width < 20 else grid_width
                                        if pos[0] > 3*ecran.get_width()/4 and pos[0] < 7*ecran.get_width()/8 and pos[1] > ecran.get_height()/3 and pos[1] < 2*ecran.get_height()/3:
                                                grid_height = grid_height - 1 if grid_height > 2 else grid_height
                                        if pos[0] > 7*ecran.get_width()/8 and pos[0] < ecran.get_width() and pos[1] > ecran.get_height()/3 and pos[1] < 2*ecran.get_height()/3:
                                                grid_height = grid_height + 1 if grid_height < 20 else grid_height
                                        if pos[0] > 3*ecran.get_width()/4 and pos[0] < ecran.get_width() and pos[1] > 2*ecran.get_height()/3 and pos[1] < ecran.get_height():
                                                start_game = True
                        if(event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)): 
                                        loop = False

                ecran.fill(white)
                                
                if game_started:
                        ecran.fill(background_color, (0, 0, image.get_width(), image.get_height()))
                        if final_time == 0 and solved(currentArray) and start_ticks>0:
                                final_time = pygame.time.get_ticks()-start_ticks
                        time_to_display = (final_time if solved(currentArray) else (pygame.time.get_ticks()-start_ticks if start_ticks>0 else 0)) // 1000
                        display_game_interface(ecran, showing_score, move_count, showing_time, time_to_display, solved(currentArray))
                        if showing_hint:
                                showHint(ecran, image)
                        else:
                                newProgress = displayAllTiles(ecran, image, currentArray, tileWidth, tileHeight, grid_width, grid_height, showing_figures, currentMovement)
                                if currentMovement[0] != 0:
                                        currentMovement = (newProgress, currentMovement[1], currentMovement[2])
                                        if isMovementOver(currentMovement, tileWidth, tileHeight, grid_width):
                                                currentArray[currentMovement[2]] = currentArray[currentMovement[1]]
                                                currentArray[currentMovement[1]] = (grid_width * grid_height) - 1
                                                currentMovement = (0,0,0)

                else:
                        if start_game:
                                image = pygame.image.load('images/image' + str(imageIndex+1) + '.jpg')
                                image = pygame.transform.scale(image, getImageSize(image.get_width(), image.get_height(), grid_width, grid_height))
                                tileWidth = image.get_width()/grid_width
                                tileHeight = image.get_height()/grid_height
                                ecran = pygame.display.set_mode((image.get_width() + 100, image.get_height()))

                                background_color = white
                                start_ticks = 0
                                final_time = 0
                                seconds = 0
                                move_count = 0
                                showing_hint = False
                                showing_figures = False
                                showing_score = True
                                showing_time = True
        
                                currentArray = getRandomArray(grid_width, grid_height)
                                currentMovement = (0, 0, 0)
                                game_started = True
                        else:
                                for i in range(3):
                                        for j in range(4):
                                                if i+3*j + firstListIndex > len(imageList)-1:
                                                        continue
                                                tempImage = imageList[i+3*j + firstListIndex]
                                                ecran.blit(tempImage, (i*ecran.get_width()/4,j*ecran.get_height()/4), (0,0,ecran.get_width()/4,ecran.get_height()/4))
                                display_start_interface(ecran, imageIndex - firstListIndex, grid_width, grid_height)
                pygame.display.update()
        pygame.quit()

playGame()

