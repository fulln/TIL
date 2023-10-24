---
dg-publish: true
title: godot-新手教程
createTime: 2023-10-23 22:27
tags:
  - godot
  - 游戏
---
## 主要流程

- [Setting up the project](https://docs.godotengine.org/en/stable/getting_started/first_2d_game/01.project_setup.html)
- [Creating the player scene](https://docs.godotengine.org/en/stable/getting_started/first_2d_game/02.player_scene.html)
- [Coding the player](https://docs.godotengine.org/en/stable/getting_started/first_2d_game/03.coding_the_player.html)
- [Creating the enemy](https://docs.godotengine.org/en/stable/getting_started/first_2d_game/04.creating_the_enemy.html)
- [The main game scene](https://docs.godotengine.org/en/stable/getting_started/first_2d_game/05.the_main_game_scene.html)
- [Heads up display](https://docs.godotengine.org/en/stable/getting_started/first_2d_game/06.heads_up_display.html)
- [Finishing up](https://docs.godotengine.org/en/stable/getting_started/first_2d_game/07.finishing-up.html)


### 构建项目

0. 下载[字体和图片资源](https://github.com/godotengine/godot-docs-project-starters/releases/download/latest-4.x/dodge_the_creeps_2d_assets.zip)

1. 设置屏幕分辨率
> 在`project settings` 的`window` 中设置长宽 ， "Viewport Width" to `480` and "Viewport Height" to `720`.

2. 在 `window` 下面的扩展选项中，设置`Mode` 为 `canvas_items` 

#### 组织项目成员

1. 构建3个独立场景 `Player`, `Mob`, and `HUD` ，后续会用到`main` 场景下

##### 创建玩家场景

1. 选择节点结构：  [Area2D](https://docs.godotengine.org/en/stable/classes/class_area2d.html#class-area2d)
2. 创建`Player` 场景，并且重置场景大小
3. 创建`Player`子场景,选择节点结构： [AnimatedSprite2D](https://docs.godotengine.org/en/stable/classes/class_animatedsprite2d.html#class-animatedsprite2d)， 用来做动画资源
4. 创建资源[SpriteFrames](https://docs.godotengine.org/en/stable/classes/class_spriteframes.html#class-spriteframes)，这个按钮在`AnimatedSprite2D` 下的 Animation 里面
5. 命名2个Frames，一个叫walk，一个叫up，把`art` 中的4个资源贴过来
6. 图片太大了，需要调整大小。点击在`AnimatedSprite2D` 下的 `Node2D` -> `Transform` ，调整Scale为`0.5,0.5`
7. 在`Player` 下面添加 [CollisionShape2D](https://docs.godotengine.org/en/stable/classes/class_collisionshape2d.html#class-collisionshape2d)子场景，这个是用来创建物品边界的node，创建一个`CapsuleShape2D` 的节点，然后调整边界大小，覆盖图片大小

 ###### 设置Player脚本
1. 设置全局变量
```scpipt
extends Area2D

@export var speed = 400 # How fast the player will move (pixels/sec).
var screen_size # Size of the game window.
```

2. 设置初始化方法，初始化下屏幕大小
```
func _ready():
	screen_size = get_viewport_rect().size
```

3. 设置处理方法， 这个方法来定义用户怎么操控这个游戏，

> 项目设置，将所有输入map定义好，映射用户的操作按钮上
