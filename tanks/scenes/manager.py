_loaded = []


def update_and_draw_current_scene(screen):
    current = _loaded[-1]
    current.update()
    if current == _loaded[-1]:  # if scene have not changed during update
        current.draw(screen)


def load_scene(scene):
    _loaded.append(scene)


def unload_current_scene():
    if len(_loaded) == 0:
        return
    _loaded.pop(-1).teardown()
