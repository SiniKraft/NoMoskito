import pygame
import pygame.gfxdraw
import ptext

popup_image = pygame.Surface((920, 540))  # Set at x = 160, y = 90
popup_image.fill((206, 237, 31))
pygame.gfxdraw.box(popup_image, pygame.rect.Rect(3, 3, 914, 50), (220, 242, 96))
pygame.gfxdraw.box(popup_image, pygame.rect.Rect(3, 53, 914, 484), (235, 248, 165))


def trailer(screen: pygame.Surface, seg_ui: pygame.font.Font, csm_40: pygame.font.Font, default_lang):
    loop = True
    continuer = True
    btn_list = [
        # DialogButton((1009, 96), (1074, 138), u"\u00D7", "close", seg_ui, screen)s
        DialogButton((363, 572), (901, 617), default_lang[79], "begin", None, screen)
    ]
    title_image = csm_40.render(default_lang[78], True, (153, 153, 0))
    title_image_rect = title_image.get_rect()
    title_image_rect.centerx, title_image_rect.centery = (640, 115)
    content_text = ""
    for t in range(0, 14):
        content_text = content_text + default_lang[t + 64]
    content_image = ptext.getsurf(content_text, color=(153, 153, 0), fontname="ComicSansMSM.ttf", fontsize=22)
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                continuer = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in btn_list:
                    if btn.isHovered:
                        btn.custom_action()
        screen.blit(popup_image, (180, 90))
        screen.blit(title_image, title_image_rect)
        screen.blit(content_image, (187, 140))
        hovered = False
        for btn in btn_list:
            if not btn.update():
                loop = False
            if btn.isHovered:
                hovered = True
        if not hovered:
            try:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            except:
                pass
        pygame.display.update()
    return continuer


class DialogButton(pygame.sprite.Sprite):
    def __init__(self, pos_min, pos_max, text: str, btn_type: str, seg_ui: pygame.font.Font,
                 screen: pygame.surface.Surface, font_size=30):
        super().__init__()
        self.screen = screen
        self.loop = True
        self.btn_type = btn_type
        self.isHovered = False
        if not self.btn_type == "close":
            self.text_image = ptext.getsurf(text, color=(153, 153, 0), fontname="ComicSansMSM.ttf",
                                            fontsize=font_size)
        else:
            self.text_image = seg_ui.render(text, True, (153, 153, 0))
        self.text_image_rect = self.text_image.get_bounding_rect()
        self.text_image = self.text_image.convert_alpha()
        self.pos_min = pos_min
        self.pos_max = pos_max
        self.image = pygame.Surface((pos_max[0] - pos_min[0], pos_max[1] - pos_min[1]))
        self.rect = self.image.get_rect()
        pygame.gfxdraw.rectangle(self.image, self.rect, (206, 237, 31))
        pygame.gfxdraw.rectangle(self.image, pygame.rect.Rect(1, 1, pos_max[0] - pos_min[0] - 2, pos_max[1] - pos_min[1]
                                                              - 2), (206, 237, 31))
        pygame.gfxdraw.rectangle(self.image, pygame.rect.Rect(2, 2, pos_max[0] - pos_min[0] - 4, pos_max[1] - pos_min[1]
                                                              - 4), (206, 237, 31))
        pygame.gfxdraw.box(self.image, pygame.rect.Rect(3, 3, pos_max[0] - pos_min[0] - 6, pos_max[1] - pos_min[1]
                                                        - 6), (235, 248, 165))
        self.hover_image = pygame.Surface((pos_max[0] - pos_min[0], pos_max[1] - pos_min[1]))
        self.hover_image.blit(self.image, (0, 0, 0, 0))
        pygame.gfxdraw.box(self.hover_image, pygame.rect.Rect(3, 3, pos_max[0] - pos_min[0] - 6, pos_max[1] - pos_min[1]
                                                              - 6), (220, 242, 96))

    def custom_action(self):
        if self.btn_type == "close":
            self.loop = False
        elif self.btn_type == "begin":
            self.loop = False
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def update(self):
        mouse_ = pygame.mouse.get_pos()
        if self.pos_max[0] > mouse_[0] > self.pos_min[0] and self.pos_min[1] < mouse_[1] < self.pos_max[1]:
            self.isHovered = True
            self.screen.blit(self.hover_image, self.pos_min)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            self.isHovered = False
            self.screen.blit(self.image, self.pos_min)
        self.screen.blit(self.text_image, (
            (self.pos_max[0] - self.pos_min[0]) / 2 + self.pos_min[0] - self.text_image_rect.centerx,
            (self.pos_max[1] - self.pos_min[1]) / 2 + self.pos_min[1] - self.text_image_rect.centery))
        return self.loop
