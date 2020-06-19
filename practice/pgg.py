#匯入pygame
import pygame as pg
#pygame初始化
pg.init()

#設定視窗
width, height = 640, 480                        #遊戲畫面寬和高
screen = pg.display.set_mode((width, height))   #依設定顯示視窗
pg.display.set_caption("UI design")           #設定程式標題

# 清除畫面並填滿背景色
screen.fill((255, 255, 255))

# 宣告 font 文字物件
head_font = pg.font.SysFont(None, 60)

# 渲染方法會回傳 surface 物件
text_surface = head_font.render('Hello World!', True, (0, 0, 0))

# blit 用來把其他元素渲染到另外一個 surface 上，這邊是 window 視窗
screen.blit(text_surface, (10, 10))

# 更新畫面，等所有操作完成後一次更新（若沒更新，則元素不會出現）
pg.display.update()

#關閉程式的程式碼
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
pg.quit()                
