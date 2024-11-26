import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:    (0, -5),
    pg.K_DOWN:  (0, +5),
    pg.K_LEFT:  (-5, 0),
    pg.K_RIGHT: (+5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct):
    """
    引数で与えられたRectが画面の中か外かを判定する
    引数：こうかとんRect or 爆弾Rect
    戻り値：真理値タプル（横、縦）/画面内：True, 画面外：False
    """
    yoko,tate = True,True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko,tate

def gameover(screen: pg.Surface) -> None:
    go_Surface = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(go_Surface,(0, 0, 0))
    go_Surface.set_alpha(200)  # 透明度設定
     # 泣いているこうかとん画像
    crying_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    crying_kk_left = crying_kk_img.get_rect()
    crying_kk_left.center = (WIDTH // 3 - 50, HEIGHT // 2)
    crying_kk_right = crying_kk_img.get_rect()
    crying_kk_right.center = (2 * WIDTH // 3 + 50, HEIGHT // 2)
    # フォントとテキスト
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rct = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    # 描画
    screen.blit(go_Surface, (0, 0))  # 黒い半透明の背景を描画
    screen.blit(crying_kk_img, crying_kk_left)  # 泣いているこうかとんを描画
    screen.blit(crying_kk_img, crying_kk_right)
    screen.blit(text, text_rct)  # 「Game Over」を描画
    pg.display.update()
    time.sleep(5)  # 5秒間停止

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    accs = [a for a in range(1, 11)]  # 加速度リスト
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))  # 可変サイズの爆弾Surface
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)  # 円を描く
        bb_img.set_colorkey((0, 0, 0))  # 黒を透過色に設定
        bb_imgs.append(bb_img)  # リストに追加
    return bb_imgs, accs

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bb_imgs, bb_accs = init_bb_imgs()

    vx, vy = 5, 5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return  # ゲームオーバー
            
        screen.blit(bg_img, [0, 0]) 

        # 時間に応じて爆弾のサイズと加速度を変更
        avx = vx * bb_accs[min(tmr // 500, 9)]  # 加速度適用
        avy = vy * bb_accs[min(tmr // 500, 9)]
        bb_img = bb_imgs[min(tmr // 500, 9)] #爆弾拡大

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, delta in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += delta[0]
                sum_mv[1] += delta[1]

        kk_rct.move_ip(sum_mv)
        #こうかとんが画面外なら、元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()