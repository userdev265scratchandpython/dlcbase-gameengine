import ctypes
import sdl2


class Renderer:
    """
    DLCbase 2D Renderer.

    Owns the SDL2 window, rendering context, input state,
    and optional game controller.

    All coordinates are in screen pixels.
    Colors are RGB or RGBA tuples with values from 0 to 255.
    """

    def __init__(self, width=1280, height=720,
                 title="DLCbase Game", vsync=True):

        if sdl2.SDL_Init(
            sdl2.SDL_INIT_VIDEO |
            sdl2.SDL_INIT_EVENTS |
            sdl2.SDL_INIT_GAMECONTROLLER
        ) != 0:
            raise RuntimeError(self._error())

        self.running = True
        self.width = width
        self.height = height

        self.window = sdl2.SDL_CreateWindow(
            title.encode("utf-8"),
            sdl2.SDL_WINDOWPOS_CENTERED,
            sdl2.SDL_WINDOWPOS_CENTERED,
            width,
            height,
            sdl2.SDL_WINDOW_SHOWN |
            sdl2.SDL_WINDOW_RESIZABLE
        )

        if not self.window:
            sdl2.SDL_Quit()
            raise RuntimeError(self._error())

        flags = sdl2.SDL_RENDERER_ACCELERATED

        if vsync:
            flags |= sdl2.SDL_RENDERER_PRESENTVSYNC

        self.renderer = sdl2.SDL_CreateRenderer(
            self.window, -1, flags
        )

        if not self.renderer:
            sdl2.SDL_DestroyWindow(self.window)
            sdl2.SDL_Quit()
            raise RuntimeError(self._error())

        sdl2.SDL_SetRenderDrawBlendMode(
            self.renderer, sdl2.SDL_BLENDMODE_BLEND
        )

        self._keys_down = set()
        self._keys_pressed = set()
        self._keys_released = set()

        self._mouse_pressed = set()
        self._mouse_released = set()

        self._textures = []
        self._controller = None

        self._controller_buttons = {
            "A": sdl2.SDL_CONTROLLER_BUTTON_A,
            "B": sdl2.SDL_CONTROLLER_BUTTON_B,
            "X": sdl2.SDL_CONTROLLER_BUTTON_X,
            "Y": sdl2.SDL_CONTROLLER_BUTTON_Y,
            "BACK": sdl2.SDL_CONTROLLER_BUTTON_BACK,
            "START": sdl2.SDL_CONTROLLER_BUTTON_START,
            "LEFT_SHOULDER":
                sdl2.SDL_CONTROLLER_BUTTON_LEFTSHOULDER,
            "RIGHT_SHOULDER":
                sdl2.SDL_CONTROLLER_BUTTON_RIGHTSHOULDER,
        }

        self._controller_axes = {
            "LEFT_X": sdl2.SDL_CONTROLLER_AXIS_LEFTX,
            "LEFT_Y": sdl2.SDL_CONTROLLER_AXIS_LEFTY,
            "RIGHT_X": sdl2.SDL_CONTROLLER_AXIS_RIGHTX,
            "RIGHT_Y": sdl2.SDL_CONTROLLER_AXIS_RIGHTY,
            "LEFT_TRIGGER":
                sdl2.SDL_CONTROLLER_AXIS_TRIGGERLEFT,
            "RIGHT_TRIGGER":
                sdl2.SDL_CONTROLLER_AXIS_TRIGGERRIGHT,
        }

        self._open_controller()

    @staticmethod
    def _error():
        return sdl2.SDL_GetError().decode("utf-8", errors="replace")

    def _open_controller(self):
        """Open the first available compatible controller."""
        if self._controller:
            return

        for index in range(sdl2.SDL_NumJoysticks()):
            if sdl2.SDL_IsGameController(index):
                self._controller = sdl2.SDL_GameControllerOpen(index)
                if self._controller:
                    return

    def poll_events(self):
        """
        Process SDL events and update input state.

        Call once per frame, before reading input.
        Returns False when the window should close.
        """
        self._keys_pressed.clear()
        self._keys_released.clear()
        self._mouse_pressed.clear()
        self._mouse_released.clear()

        event = sdl2.SDL_Event()

        while sdl2.SDL_PollEvent(ctypes.byref(event)):
            if event.type == sdl2.SDL_QUIT:
                self.running = False

            elif event.type == sdl2.SDL_KEYDOWN:
                key = event.key.keysym.sym

                if key not in self._keys_down:
                    self._keys_pressed.add(key)

                self._keys_down.add(key)

            elif event.type == sdl2.SDL_KEYUP:
                key = event.key.keysym.sym
                self._keys_down.discard(key)
                self._keys_released.add(key)

            elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                self._mouse_pressed.add(event.button.button)

            elif event.type == sdl2.SDL_MOUSEBUTTONUP:
                self._mouse_released.add(event.button.button)

            elif event.type == sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_SIZE_CHANGED:
                    self.width = event.window.data1
                    self.height = event.window.data2

            elif event.type == sdl2.SDL_CONTROLLERDEVICEADDED:
                self._open_controller()

            elif event.type == sdl2.SDL_CONTROLLERDEVICEREMOVED:
                if self._controller:
                    instance = sdl2.SDL_JoystickInstanceID(
                        sdl2.SDL_GameControllerGetJoystick(
                            self._controller
                        )
                    )

                    if instance == event.cdevice.which:
                        sdl2.SDL_GameControllerClose(self._controller)
                        self._controller = None

        return self.running

    def _keycode(self, name):
        """Convert a key name such as SPACE or A into an SDL keycode."""
        return sdl2.SDL_GetKeyFromName(name.encode("utf-8"))

    def key_down(self, name):
        """True while a keyboard key is held."""
        return self._keycode(name) in self._keys_down

    def key_pressed(self, name):
        """True only on the frame a key is initially pressed."""
        return self._keycode(name) in self._keys_pressed

    def key_released(self, name):
        """True on the frame a key is released."""
        return self._keycode(name) in self._keys_released

    def mouse_position(self):
        """Return the current mouse position as (x, y)."""
        x = ctypes.c_int()
        y = ctypes.c_int()

        sdl2.SDL_GetMouseState(
            ctypes.byref(x), ctypes.byref(y)
        )

        return x.value, y.value

    def mouse_down(self, button="LEFT"):
        """True while a mouse button is held."""
        buttons = {
            "LEFT": sdl2.SDL_BUTTON_LEFT,
            "MIDDLE": sdl2.SDL_BUTTON_MIDDLE,
            "RIGHT": sdl2.SDL_BUTTON_RIGHT,
        }

        button_id = buttons.get(button.upper())

        if button_id is None:
            return False

        state = sdl2.SDL_GetMouseState(None, None)
        return bool(state & sdl2.SDL_BUTTON(button_id))

    def mouse_pressed(self, button="LEFT"):
        """True only on the frame a mouse button is pressed."""
        buttons = {
            "LEFT": sdl2.SDL_BUTTON_LEFT,
            "MIDDLE": sdl2.SDL_BUTTON_MIDDLE,
            "RIGHT": sdl2.SDL_BUTTON_RIGHT,
        }

        return buttons.get(button.upper()) in self._mouse_pressed

    def mouse_released(self, button="LEFT"):
        """True on the frame a mouse button is released."""
        buttons = {
            "LEFT": sdl2.SDL_BUTTON_LEFT,
            "MIDDLE": sdl2.SDL_BUTTON_MIDDLE,
            "RIGHT": sdl2.SDL_BUTTON_RIGHT,
        }

        return buttons.get(button.upper()) in self._mouse_released

    def controller_connected(self):
        """True if a compatible game controller is connected."""
        return bool(
            self._controller and
            sdl2.SDL_GameControllerGetAttached(self._controller)
        )

    def controller_button_down(self, button):
        """Check whether a controller button is held."""
        if not self.controller_connected():
            return False

        button_id = self._controller_buttons.get(button.upper())

        if button_id is None:
            return False

        return bool(
            sdl2.SDL_GameControllerGetButton(
                self._controller, button_id
            )
        )

    def controller_axis(self, axis):
        """
        Read a controller axis.

        Stick axes return approximately -1.0 to 1.0.
        Trigger axes return approximately 0.0 to 1.0.
        """
        if not self.controller_connected():
            return 0.0

        axis_id = self._controller_axes.get(axis.upper())

        if axis_id is None:
            return 0.0

        value = sdl2.SDL_GameControllerGetAxis(
            self._controller, axis_id
        )

        if "TRIGGER" in axis.upper():
            return max(0.0, value / 32767.0)

        return value / 32768.0

    def clear(self, color=(0, 0, 0)):
        """Clear the frame with an RGB or RGBA color."""
        r, g, b = color[:3]
        a = color[3] if len(color) == 4 else 255

        sdl2.SDL_SetRenderDrawColor(
            self.renderer, r, g, b, a
        )

        sdl2.SDL_RenderClear(self.renderer)

    def draw_rect(self, x, y, width, height,
                  color=(255, 255, 255), filled=True):
        """Draw a filled or outlined rectangle."""
        r, g, b = color[:3]
        a = color[3] if len(color) == 4 else 255

        sdl2.SDL_SetRenderDrawColor(
            self.renderer, r, g, b, a
        )

        rect = sdl2.SDL_Rect(
            int(x), int(y), int(width), int(height)
        )

        if filled:
            sdl2.SDL_RenderFillRect(
                self.renderer, ctypes.byref(rect)
            )
        else:
            sdl2.SDL_RenderDrawRect(
                self.renderer, ctypes.byref(rect)
            )

    def draw_line(self, x1, y1, x2, y2,
                  color=(255, 255, 255)):
        """Draw a line between two points."""
        r, g, b = color[:3]
        a = color[3] if len(color) == 4 else 255

        sdl2.SDL_SetRenderDrawColor(
            self.renderer, r, g, b, a
        )

        sdl2.SDL_RenderDrawLine(
            self.renderer,
            int(x1), int(y1), int(x2), int(y2)
        )

    def load_texture(self, path):
        """
        Load a BMP texture.

        Returns an opaque texture handle.
        """
        surface = sdl2.SDL_LoadBMP(
            path.encode("utf-8")
        )

        if not surface:
            raise RuntimeError(self._error())

        texture = sdl2.SDL_CreateTextureFromSurface(
            self.renderer, surface
        )

        sdl2.SDL_FreeSurface(surface)

        if not texture:
            raise RuntimeError(self._error())

        self._textures.append(texture)
        return texture

    def draw_texture(self, texture, x, y,
                     width=None, height=None, angle=0):
        """Draw a texture, optionally scaling and rotating it."""
        if width is None or height is None:
            w = ctypes.c_int()
            h = ctypes.c_int()

            if sdl2.SDL_QueryTexture(
                texture, None, None,
                ctypes.byref(w), ctypes.byref(h)
            ) != 0:
                raise RuntimeError(self._error())

            width = w.value
            height = h.value

        dest = sdl2.SDL_Rect(
            int(x), int(y), int(width), int(height)
        )

        result = sdl2.SDL_RenderCopyEx(
            self.renderer,
            texture,
            None,
            ctypes.byref(dest),
            float(angle),
            None,
            sdl2.SDL_FLIP_NONE
        )

        if result != 0:
            raise RuntimeError(self._error())

    def destroy_texture(self, texture):
        """Destroy a texture created by load_texture()."""
        if texture in self._textures:
            sdl2.SDL_DestroyTexture(texture)
            self._textures.remove(texture)

    def present(self):
        """Present the completed frame."""
        sdl2.SDL_RenderPresent(self.renderer)

    def close(self):
        """Release resources and close SDL2."""
        for texture in self._textures:
            sdl2.SDL_DestroyTexture(texture)

        self._textures.clear()

        if self._controller:
            sdl2.SDL_GameControllerClose(self._controller)
            self._controller = None

        if self.renderer:
            sdl2.SDL_DestroyRenderer(self.renderer)
            self.renderer = None

        if self.window:
            sdl2.SDL_DestroyWindow(self.window)
            self.window = None

        sdl2.SDL_Quit()
        self.running = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
