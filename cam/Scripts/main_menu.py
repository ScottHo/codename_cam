from component import *
from controller import *
from physics import *
from ui import *
from entity import *

import sys
import os
sys.path.insert(0, os.getcwd() + "\..\..\cam\Scripts")
from runner_ai import *
from camera_control import *

def set_position(marker, item):
    marker.position = item.position + Vec2(-0.2, 0.0)

class MainMenu:
    def start_game(self):
        e = self.entity

        while e.get_parent():
            e = e.get_parent()

        level = Entity.create(e).lock()
        mesh = Mesh(ModelShader("map_texture.jpg"), "map_mesh.fbx", Vec3(0.2, 0.4, 0.2), Vec3(2.0, 2.0, 2.0), 4) # TODO hacky hacky hardcoded opengl constant, 4 is GL_TRIANGLES
        body = RigidBody(self.physics, "map_mesh.fbx", 2.0, False)
        level.add_component(mesh)
        level.add_component(body)

        ai = Entity.create(e).lock()
        mesh = Mesh(ModelShader("chaser_texture.jpg"), "chaser_mesh.fbx", Vec3(1.0, 0.84, 0.0), Vec3(1, 1, 1), 4)
        vehicle = ScriptComponent("chaser_ai", self.physics)
        chaser = ScriptComponent("chaser", self.physics)
        ai.add_component(mesh)
        ai.add_component(vehicle)
        ai.add_component(chaser)

        player = Entity.create(e).lock()
        vehicle = ScriptComponent("vehicle_script", self.physics)
        player.add_component(vehicle)
        player.add_component(ScriptComponent("powerup_manager", self.physics))

        cam = Entity.create(e).lock()
        cam.global_position = player.global_position + Vec3(0.0, 10.0, -30)
        cam.add_component(CameraControl(player), self.physics)

        runner = Entity.create(e).lock()
        runner.add_component(Mesh(ModelShader("runner_texture_green.jpg"), "runner_mesh.fbx", Vec3(1.0, 0.84, 0.0), Vec3(1, 1, 1), 4))
        runner.add_component(RunnerAi(Vec3(10.0, 2.0, -100.0)), self.physics)

        runner2 = Entity.create(e).lock()
        runner2.add_component(Mesh(ModelShader("runner_texture_green.jpg"), "runner_mesh.fbx", Vec3(1.0, 0.84, 0.0), Vec3(1, 1, 1), 4))
        runner2.add_component(RunnerAi(Vec3(-5.0, 0.0, 100.0)), self.physics)

        runner3 = Entity.create(e).lock()
        runner3.add_component(Mesh(ModelShader("runner_texture_green.jpg"), "runner_mesh.fbx", Vec3(1.0, 0.84, 0.0), Vec3(1, 1, 1), 4))
        runner3.add_component(RunnerAi(Vec3(90.0, 2.0, -10.0)), self.physics)

        runner4 = Entity.create(e).lock()
        runner4.add_component(Mesh(ModelShader("runner_texture_green.jpg"), "runner_mesh.fbx", Vec3(1.0, 0.84, 0.0), Vec3(1, 1, 1), 4))
        runner4.add_component(RunnerAi(Vec3(0.0, 2.0, -90.0)), self.physics)

        o = Entity.create(e).lock()
        o.transform().position = Vec3(0.0, 0.0, 60)
        o.add_component(ScriptComponent("oil_slick_powerup", self.physics))

        e.add_component(ScriptComponent("start_game", self.physics))

        self.entity.destroy()

    def start(self):
        self.control = Controller(0)
        self.background = Image("background.png", Vec2(-1.0, -1.0), Vec2(2.0, 2.0), 3)
        self.startgame = Text("Start Game", "GROBOLD", Vec2(-0.3, 0.0), 12)
        self.quitgame = Text("Quit Game", "GROBOLD", Vec2(-0.3, -0.2), 12)
        self.marker = Image("menu-marker.png", Vec2(-1.0, -1.0), Vec2(0.2, 0.2), 1)
        self.selected = self.startgame

        set_position(self.marker, self.startgame)

        self.entity.add_component(self.background)
        self.entity.add_component(self.startgame)
        self.entity.add_component(self.quitgame)
        self.entity.add_component(self.marker)

    def update(self, dt):
        self.control.update()
        if self.control.direction == 7: # down - probably shouldn't hardcode these...
            if self.selected != self.quitgame:
                self.selected = self.quitgame
                set_position(self.marker, self.quitgame)
        elif self.control.direction == 6:
            if self.selected != self.startgame:
                self.selected = self.startgame
                set_position(self.marker, self.startgame)

        if self.control.select:
            if self.selected == self.startgame:
                self.start_game()
