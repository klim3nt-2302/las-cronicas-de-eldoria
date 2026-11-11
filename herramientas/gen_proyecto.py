"""Genera el proyecto GDevelop 5 (game.json) de «Las Crónicas de Eldoria».

Uso:  python3 herramientas/gen_proyecto.py   (desde la carpeta Eldoria)
Requiere haber ejecutado antes gen_imagenes.py y gen_audio.py.
"""
import json
import os
import struct
import uuid

ROOT = os.path.join(os.path.dirname(__file__), '..')
SPR = 'assets/sprites/'
AUD = 'assets/audio/'
PORTADA = 'assets/portada/portada.png'
W, H = 960, 540
GROUND = 432          # altura (y) del suelo normal
LEVEL_W = 4800        # 5 pantallas de 960 px por nivel → 10 pantallas en total


def uid():
    return str(uuid.uuid4())


def png_size(name):
    with open(os.path.join(ROOT, SPR, name), 'rb') as f:
        f.read(16)
        return struct.unpack('>II', f.read(8))


# ====================================================================== Recursos
resources = []


def add_resources():
    for f in sorted(os.listdir(os.path.join(ROOT, SPR))):
        if f.endswith('.png'):
            resources.append({"alwaysLoaded": False, "file": SPR + f, "kind": "image", "metadata": "",
                              "name": SPR + f, "smoothed": False, "userAdded": True})
    if os.path.exists(os.path.join(ROOT, PORTADA)):
        resources.append({"alwaysLoaded": False, "file": PORTADA, "kind": "image", "metadata": "",
                          "name": PORTADA, "smoothed": False, "userAdded": True})
    for f in sorted(os.listdir(os.path.join(ROOT, AUD))):
        if f.endswith('.wav'):
            music = f.startswith('musica_') or f.startswith('ambiente_')
            resources.append({"file": AUD + f, "kind": "audio", "metadata": "", "name": AUD + f,
                              "preloadAsMusic": music, "preloadAsSound": not music,
                              "preloadInCache": False, "userAdded": True})


# ====================================================================== Objetos
def frame(img, mask=None):
    spr = {"hasCustomCollisionMask": mask is not None, "image": SPR + img, "points": [],
           "originPoint": {"name": "origine", "x": 0, "y": 0},
           "centerPoint": {"automatic": True, "name": "centre", "x": 0, "y": 0},
           "customCollisionMask": []}
    if mask:
        x0, y0, x1, y1 = mask
        spr["customCollisionMask"] = [[{"x": x0, "y": y0}, {"x": x1, "y": y0},
                                       {"x": x1, "y": y1}, {"x": x0, "y": y1}]]
    return spr


def var(name, value):
    if isinstance(value, str):
        return {"name": name, "type": "string", "value": value}
    return {"name": name, "type": "number", "value": value}


def sprite(name, anims, behaviors=(), variables=(), mask=None):
    """anims: lista de (nombre, [imagenes], segundos_entre_frames, bucle)."""
    return {
        "adaptCollisionMaskAutomatically": False, "assetStoreId": "", "name": name,
        "persistentUuid": uid(), "type": "Sprite", "updateIfNotVisible": False,
        "variables": [var(k, v) for k, v in variables], "effects": [], "behaviors": list(behaviors),
        "animations": [{"name": an, "useMultipleDirections": False, "directions": [
            {"looping": loop, "timeBetweenFrames": t, "sprites": [frame(i, mask) for i in imgs]}]}
            for (an, imgs, t, loop) in anims],
    }


def tiled(name, texture, behaviors=()):
    w, h = png_size(texture)
    return {"assetStoreId": "", "height": h, "name": name, "persistentUuid": uid(),
            "texture": SPR + texture, "type": "TiledSpriteObject::TiledSprite", "width": w,
            "variables": [], "effects": [], "behaviors": list(behaviors)}


def text(name, string, size=24, color="255;255;255", bold=True, outline=True):
    r, g, b = [int(c) for c in color.split(';')]
    return {
        "assetStoreId": "", "bold": bold, "italic": False, "name": name, "persistentUuid": uid(),
        "smoothed": True, "type": "TextObject::Text", "underlined": False, "variables": [],
        "effects": [], "behaviors": [], "string": string, "font": "", "textAlignment": "left",
        "characterSize": size, "color": {"r": r, "g": g, "b": b},
        "content": {
            "bold": bold, "isOutlineEnabled": outline, "isShadowEnabled": True, "italic": False,
            "outlineColor": "20;12;36", "outlineThickness": 3, "shadowAngle": 90,
            "shadowBlurRadius": 2, "shadowColor": "0;0;0", "shadowDistance": 3, "shadowOpacity": 127,
            "smoothed": True, "underlined": False, "text": string, "font": "",
            "textAlignment": "left", "verticalTextAlignment": "top", "characterSize": size,
            "lineHeight": 0, "color": color},
    }


PLATFORM = {"name": "Platform", "type": "PlatformBehavior::PlatformBehavior", "canBeGrabbed": False,
            "platformType": "NormalPlatform", "yGrabOffset": 0}
JUMPTHRU = dict(PLATFORM, platformType="Jumpthru")
PLATFORMER = {
    "name": "PlatformerObject", "type": "PlatformBehavior::PlatformerObjectBehavior",
    "canGoDownFromJumpthru": True, "acceleration": 1500, "deceleration": 1800, "gravity": 1500,
    "jumpSpeed": 720, "jumpSustainTime": 0.15, "ladderClimbingSpeed": 150, "maxFallingSpeed": 800,
    "maxSpeed": 270, "canGrabPlatforms": False, "ignoreDefaultControls": False, "slopeMaxAngle": 60,
    "useLegacyTrajectory": False, "xGrabTolerance": 10, "yGrabOffset": 0,
}


def lyra_obj(name="Lyra", platformer=True):
    return sprite(name, [
        ("Quieto", ["lyra_quieto1.png"] * 6 + ["lyra_quieto2.png"], 0.2, True),
        ("Correr", ["lyra_correr%d.png" % i for i in range(1, 5)], 0.09, True),
        ("Saltar", ["lyra_saltar.png"], 0.1, False),
    ], behaviors=[PLATFORMER] if platformer else [], mask=(9, 6, 39, 72))


def global_objects():
    return [
        lyra_obj(),
        sprite("Goblin", [("Caminar", ["goblin1.png", "goblin2.png"], 0.18, True)],
               variables=[("dir", 1), ("vel", 70), ("minX", 0), ("maxX", 0), ("alerta", 0), ("cerca", 0)],
               mask=(6, 6, 42, 48)),
        sprite("Murcielago", [("Volar", ["murcielago1.png", "murcielago2.png"], 0.14, True)],
               variables=[("dir", 1), ("minX", 0), ("maxX", 0), ("baseY", 200), ("alerta", 0), ("cerca", 0)],
               mask=(6, 6, 42, 30)),
        sprite("Gema", [("Brillo", ["gema%d.png" % i for i in range(1, 5)], 0.15, True)]),
        sprite("Corazon", [("Latido", ["corazon.png"], 0.1, False)]),
        sprite("Destello", [("Destello", ["destello%d.png" % i for i in range(1, 5)], 0.07, False)]),
        sprite("Humo", [("Humo", ["humo%d.png" % i for i in range(1, 5)], 0.08, False)]),
        sprite("IconoE", [("E", ["icono_e.png"], 0.1, False)]),
        sprite("Cartel", [("Cartel", ["cartel.png"], 0.1, False)], variables=[("texto", "")]),
        tiled("Pinchos", "pinchos.png"),
        sprite("Bandera", [("apagada", ["bandera_apagada.png"], 0.1, False),
                           ("encendida", ["bandera_encendida.png"], 0.1, False)]),
        sprite("Hongo", [("Normal", ["hongo1.png"], 0.1, False), ("Rebote", ["hongo2.png"], 0.1, False)]),
        sprite("Negro", [("Negro", ["negro.png"], 0.1, False)]),
        sprite("Blanco", [("Blanco", ["blanco.png"], 0.1, False)]),
        sprite("Vidas", [("v%d" % i, ["hud_vidas%d.png" % i], 0.1, False) for i in range(4)]),
        sprite("IconoGema", [("Gema", ["gema1.png"], 0.1, False)]),
        sprite("IconoLlave", [("Llave", ["llave.png"], 0.1, False)]),
        sprite("CajaDialogo", [("Caja", ["caja_dialogo.png"], 0.1, False)]),
        text("TextoGemas", "x 0", 26),
        text("TextoNivel", "", 20, "255;232;160"),
        text("Mensaje", "", 22, "255;246;216"),
        text("NombreDialogo", "", 22, "255;216;74"),
        text("TextoDialogo", "", 20, "255;255;255", bold=False, outline=False),
        text("TextoContinuar", "[E] continuar", 16, "190;190;220", bold=False, outline=False),
    ]


# ====================================================================== Instancias
class Scene:
    def __init__(self, name, color=(0, 0, 0)):
        self.name = name
        self.color = color
        self.objects = []
        self.instances = []
        self.events = []
        self.variables = []
        self.groups = []
        self.layers = ["Fondo", "", "HUD"]

    def inst(self, obj, x, y, layer="", w=None, h=None, z=10, **vars):
        i = {"angle": 0, "customSize": w is not None, "height": h or 0, "layer": layer, "name": obj,
             "persistentUuid": uid(), "width": w or 0, "x": x, "y": y, "zOrder": z,
             "numberProperties": [], "stringProperties": [],
             "initialVariables": [var(k, v) for k, v in vars.items()]}
        if w is not None:
            i["depth"] = 0
        self.instances.append(i)
        return i


# ====================================================================== Eventos (mini-DSL)
def I(kind, *params, inv=False, sub=None):
    ins = {"type": {"value": kind}, "parameters": [str(p) for p in params]}
    if inv:
        ins["type"]["inverted"] = True
    if sub is not None:
        ins["subInstructions"] = sub
    return ins


def ev(conds, acts, events=None):
    e = {"type": "BuiltinCommonInstructions::Standard", "conditions": conds, "actions": acts}
    if events:
        e["events"] = events
    return e


def foreach(obj, events, conds=(), acts=()):
    return {"type": "BuiltinCommonInstructions::ForEach", "object": obj,
            "conditions": list(conds), "actions": list(acts), "events": events}


def group(name, events, color=(52, 73, 94)):
    return {"colorB": color[2], "colorG": color[1], "colorR": color[0], "creationTime": 0,
            "name": name, "source": "", "type": "BuiltinCommonInstructions::Group",
            "events": events, "parameters": []}


def comment(txt):
    return {"type": "BuiltinCommonInstructions::Comment",
            "color": {"b": 109, "g": 230, "r": 255, "textB": 0, "textG": 0, "textR": 0},
            "comment": txt}


def s(txt):
    """Literal de texto para expresiones de GDevelop (con saltos de línea)."""
    parts = txt.split('\n')
    return ' + NewLine() + '.join('"%s"' % p.replace('\\', '\\\\').replace('"', '\\"') for p in parts)


ONCE = I("BuiltinCommonInstructions::Once")
def num(v, op, val): return I("NumberVariable", v, op, val)
def setn(v, op, val): return I("SetNumberVariable", v, op, val)
def cmp(a, op, b): return I("BuiltinCommonInstructions::CompareNumbers", a, op, b)
def ovar(o, v, op, val): return I("VarObjet", o, v, op, val)
def setov(o, v, op, val): return I("ModVarObjet", o, v, op, val)
def coll(a, b): return I("CollisionNP", a, b, "", "", "")
def key(k): return I("KeyPressed", "", k)
def sound(f, vol=60, pitch="1"): return I("PlaySound", "", AUD + f, "", vol, pitch)
def music(f, ch=1, loop=True, vol=45): return I("PlayMusicOnChannel", "", AUD + f, ch, "yes" if loop else "no", vol, 1)
def ambient(f, ch=2, vol=35): return I("PlaySoundOnChannel", "", AUD + f, ch, "yes", vol, 1)
def settext(o, expr): return I("TextContainerCapability::TextContainerBehavior::SetValue", o, "Text", "=", expr)
def anim(o, name): return I("AnimatableCapability::AnimatableBehavior::SetName", o, "Animation", "=", '"%s"' % name)
def is_anim(o, name, inv=False): return I("AnimatableCapability::AnimatableBehavior::Name", o, "Animation", "=", '"%s"' % name, inv=inv)
def flip(o, yes): return I("FlippableCapability::FlippableBehavior::FlipX", o, "Flippable", "yes" if yes else "no")
def hide(o): return I("Hide", o)
def show(o): return I("Show", o, "")
def opacity(o, op, val): return I("Opacity", o, op, val)
def reset_timer(t): return I("ResetTimer", "", '"%s"' % t)
def timer(t, op, val): return I("CompareTimer", "", '"%s"' % t, op, val)
def otimer(o, t, op, val): return I("CompareObjectTimer", o, '"%s"' % t, op, val)
def reset_otimer(o, t): return I("ResetObjectTimer", o, '"%s"' % t)
def goto(scene): return I("Scene", "", '"%s"' % scene, "")
def create(o, x, y, layer=""): return I("Create", "", o, x, y, layer)
def delete(o): return I("Delete", o, "")
def pb(action, *p): return I("PlatformBehavior::" + action, "Lyra", "PlatformerObject", *p)
def near(a, b, dx, dy):
    return [cmp("abs(%s.CenterX() - %s.CenterX())" % (a, b), "<", dx),
            cmp("abs(%s.CenterY() - %s.CenterY())" % (a, b), "<", dy)]
def message(txt):
    return [settext("Mensaje", s(txt)), reset_timer("msg")]
def pressed_any(*keys):
    return I("BuiltinCommonInstructions::Or", sub=[key(k) for k in keys])


# ====================================================================== Escenas de nivel
def hud(scene, titulo, con_llave):
    scene.inst("Vidas", 20, 16, "HUD", z=50)
    scene.inst("IconoGema", 20, 52, "HUD", z=50)
    scene.inst("TextoGemas", 64, 48, "HUD", z=50)
    if con_llave:
        scene.inst("IconoLlave", 20, 92, "HUD", z=50)
    t = scene.inst("TextoNivel", 600, 16, "HUD", z=50)
    scene.inst("Mensaje", 300, 92, "HUD", z=55)
    scene.inst("CajaDialogo", 30, 388, "HUD", z=60)
    scene.inst("NombreDialogo", 60, 398, "HUD", z=61)
    scene.inst("TextoDialogo", 60, 430, "HUD", z=61)
    scene.inst("TextoContinuar", 790, 498, "HUD", z=61)
    scene.inst("Negro", 0, 0, "HUD", W, H, z=100)
    scene.titulo = titulo


def fondo(scene, prefix, layers):
    scene.objects.append(sprite("Cielo", [("Cielo", ["%s_%s.png" % (prefix, layers[0])], 0.1, False)]))
    scene.inst("Cielo", 0, 0, "Fondo", z=1)
    for i, (lname, oname) in enumerate(layers[1:]):
        scene.objects.append(tiled(oname, "%s_%s.png" % (prefix, lname)))
        scene.inst(oname, 0, 0, "Fondo", W, H, z=2 + i)


def ground(scene, obj, segments):
    for (x, w, top) in segments:
        scene.inst(obj, x, top, w=w, h=288, z=5)


def common_level_events(scene, musica, ambiente, fondo_objs, nivel):
    ev_inicio = group("Inicio del nivel", [
        comment("Música incidental en el canal 1 y sonido ambiental en bucle en el canal 2. "
                "El punto de reaparición inicial es la posición de Lyra."),
        ev([I("SceneJustBegins", "")], [
            music(musica), ambient(ambiente),
            reset_timer("inv"), reset_timer("msg"), reset_otimer("Lyra", "paso"),
            setn("CheckX", "=", "Lyra.X()"), setn("CheckY", "=", "Lyra.Y()"),
            setn("NivelActual", "=", nivel),
            hide("CajaDialogo"), hide("TextoDialogo"), hide("NombreDialogo"), hide("TextoContinuar"),
            hide("IconoE"), hide("IconoLlave"),
            settext("TextoNivel", s(scene.titulo)), settext("Mensaje", '""'),
            opacity("Negro", "=", 255),
        ]),
        ev([opacity("Negro", ">", 0), num("Saliendo", "=", 0)], [opacity("Negro", "-", "350 * TimeDelta()")]),
        ev([num("Saliendo", "=", 1)], [opacity("Negro", "+", "250 * TimeDelta()")]),
    ], (41, 128, 185))

    ev_controles = group("Controles del avatar", [
        comment("Flechas + Espacio son los controles por defecto del comportamiento Plataformero. "
                "Aquí añadimos WASD, la flecha arriba para saltar y la tecla de interacción (E o Enter)."),
        ev([num("Dialogo", "=", 0), key("a")], [pb("SimulateLeftKey")]),
        ev([num("Dialogo", "=", 0), key("d")], [pb("SimulateRightKey")]),
        ev([num("Dialogo", "=", 0), pressed_any("w", "Up")], [pb("SimulateJumpKey")]),
        ev([pressed_any("e", "Return"), ONCE], [setn("Accion", "=", 1)]),
        ev([I("BuiltinCommonInstructions::Or", sub=[cmp("Variable(Dialogo)", ">", 0), num("Saliendo", "=", 1)])],
           [pb("IgnoreDefaultControls", "yes")]),
        ev([num("Dialogo", "=", 0), num("Saliendo", "=", 0)], [pb("IgnoreDefaultControls", "no")]),
    ], (39, 174, 96))

    ev_anim = group("Animación y sonidos del avatar", [
        ev([I("PlatformBehavior::IsOnFloor", "Lyra", "PlatformerObject"),
            I("PlatformBehavior::PlatformerObjectBehavior::IsMovingEvenALittle", "Lyra", "PlatformerObject")],
           [anim("Lyra", "Correr")], [
            comment("Sonido de pasos: uno cada 0,28 s mientras camina, con tono ligeramente aleatorio."),
            ev([otimer("Lyra", "paso", ">=", "0.28")],
               [sound("paso.wav", 35, "RandomFloatInRange(0.85, 1.15)"), reset_otimer("Lyra", "paso")]),
        ]),
        ev([I("PlatformBehavior::IsOnFloor", "Lyra", "PlatformerObject"),
            I("PlatformBehavior::PlatformerObjectBehavior::IsMovingEvenALittle", "Lyra", "PlatformerObject", inv=True)],
           [anim("Lyra", "Quieto")]),
        ev([I("PlatformBehavior::IsOnFloor", "Lyra", "PlatformerObject", inv=True)], [anim("Lyra", "Saltar")]),
        ev([I("PlatformBehavior::PlatformerObjectBehavior::IsUsingControl", "Lyra", "PlatformerObject", '"Left"')],
           [flip("Lyra", True)]),
        ev([I("PlatformBehavior::PlatformerObjectBehavior::IsUsingControl", "Lyra", "PlatformerObject", '"Right"')],
           [flip("Lyra", False)]),
        ev([I("PlatformBehavior::IsJumping", "Lyra", "PlatformerObject"), ONCE], [sound("salto.wav", 40)]),
        ev([I("PlatformBehavior::IsOnFloor", "Lyra", "PlatformerObject")], [pb("JumpSpeed", "=", 720)]),
    ], (142, 68, 173))

    xoffs = [I("TiledSpriteObject::XOffset", o, "=", 'CameraCenterX("") * %s' % f) for (o, f) in fondo_objs]
    ev_camara = group("Cámara y parallax", [
        comment("La cámara sigue a Lyra sin salir de los límites del nivel (5 pantallas de ancho). "
                "Las capas del fondo se desplazan más lento para dar profundidad (parallax)."),
        ev([], [I("CenterCameraOnObject", "", "Lyra", "", "", ""),
                I("ClampCamera", "", 0, 0, LEVEL_W, H, "", "")] + xoffs),
    ], (22, 160, 133))

    ev_items = group("Objetos recolectables", [
        ev([coll("Lyra", "Gema")], [
            create("Destello", "Gema.CenterX() - 18", "Gema.CenterY() - 18"), delete("Gema"),
            setn("Gemas", "+", 1), sound("gema.wav", 45)]),
        ev([coll("Lyra", "Corazon")], [
            create("Destello", "Corazon.CenterX() - 18", "Corazon.CenterY() - 18"), delete("Corazon"),
            setn("Vidas", "+", 1), sound("curar.wav", 50)] + message("¡Vida extra!")),
        ev([num("Vidas", ">", 3)], [setn("Vidas", "=", 3)]),
        ev([I("AnimationEnded", "Destello")], [delete("Destello")]),
        ev([I("AnimationEnded", "Humo")], [delete("Humo")]),
    ], (241, 196, 15))

    ev_hongo = group("Entorno: hongos, pinchos, carteles y punto de control", [
        comment("Hongo mágico: si Lyra cae sobre él, sale impulsada muy alto."),
        ev([coll("Lyra", "Hongo"), I("PlatformBehavior::IsFalling", "Lyra", "PlatformerObject")], [
            pb("JumpSpeed", "=", 1050), pb("SetCanJump"), pb("SimulateJumpKey"),
            anim("Hongo", "Rebote"), reset_otimer("Hongo", "rebote"), sound("hongo.wav", 55)]),
        ev([is_anim("Hongo", "Rebote"), otimer("Hongo", "rebote", ">=", "0.2")], [anim("Hongo", "Normal")]),
        ev([coll("Lyra", "Pinchos")], [setn("Danio", "=", 1)]),
        ev([coll("Lyra", "Bandera"), is_anim("Bandera", "apagada")], [
            anim("Bandera", "encendida"), setn("CheckX", "=", "Bandera.X()"),
            setn("CheckY", "=", "Bandera.Y() - 8"), sound("checkpoint.wav", 55),
            create("Destello", "Bandera.X()", "Bandera.Y()")] + message("Punto de control activado")),
        comment("Carteles: al acercarse aparece el icono [E]; al pulsarla se muestra su texto."),
        foreach("Cartel", [
            ev(near("Lyra", "Cartel", 70, 80) + [num("Dialogo", "=", 0)], [
                show("IconoE"),
                I("SetXY", "IconoE", "=", "Cartel.CenterX() - 18", "=", "Cartel.Y() - 42 + sin(TimeFromStart() * 6) * 3")], [
                ev([num("Accion", "=", 1)], [
                    settext("Mensaje", "Cartel.VariableString(texto)"), reset_timer("msg"),
                    sound("cartel.wav", 45), setn("Accion", "=", 0)]),
            ]),
        ]),
    ], (211, 84, 0))

    ev_goblin = group("NPC 1 · Goblin (patrulla y persecución)", [
        comment("Cada goblin patrulla entre sus variables minX y maxX. Si Lyra se acerca (260 px en "
                "horizontal y a su misma altura) gruñe, se vuelve rojizo y la persigue al doble de "
                "velocidad, sin salir de su zona."),
        foreach("Goblin", [
            ev([], [setov("Goblin", "cerca", "=", 0), setov("Goblin", "vel", "=", 70)]),
            ev(near("Lyra", "Goblin", 260, 90), [
                setov("Goblin", "cerca", "=", 1), setov("Goblin", "vel", "=", 150),
                setov("Goblin", "dir", "=", "sign(Lyra.CenterX() - Goblin.CenterX())"),
                I("ChangeColor", "Goblin", '"255;150;150"')], [
                ev([ovar("Goblin", "alerta", "=", 0)], [sound("goblin.wav", 50), setov("Goblin", "alerta", "=", 1)]),
            ]),
            ev([ovar("Goblin", "cerca", "=", 0)], [setov("Goblin", "alerta", "=", 0),
                                                    I("ChangeColor", "Goblin", '"255;255;255"')]),
            ev([ovar("Goblin", "cerca", "=", 0), ovar("Goblin", "dir", "=", 0)], [setov("Goblin", "dir", "=", 1)]),
            ev([I("PosX", "Goblin", "<=", "Goblin.Variable(minX)"), ovar("Goblin", "dir", "<", 0)],
               [setov("Goblin", "dir", "=", "1 - Goblin.Variable(cerca)")]),
            ev([I("PosX", "Goblin", ">=", "Goblin.Variable(maxX)"), ovar("Goblin", "dir", ">", 0)],
               [setov("Goblin", "dir", "=", "Goblin.Variable(cerca) - 1")]),
            ev([], [I("AddForceXY", "Goblin", "Goblin.Variable(dir) * Goblin.Variable(vel)", 0, 0)]),
            ev([ovar("Goblin", "dir", "<", 0)], [flip("Goblin", True)]),
            ev([ovar("Goblin", "dir", ">", 0)], [flip("Goblin", False)]),
        ]),
    ], (39, 174, 96))

    dist = "DistanceBetweenPositions(Lyra.CenterX(), Lyra.CenterY(), Murcielago.CenterX(), Murcielago.CenterY())"
    ev_bat = group("NPC 2 · Murciélago (vuelo ondulante y ataque en picada)", [
        comment("Vuela de lado a lado ondulando sobre su altura base. Cuando Lyra entra en un radio de "
                "280 px chilla y se lanza directamente hacia ella; si se aleja, vuelve a su ruta."),
        foreach("Murcielago", [
            ev([], [setov("Murcielago", "cerca", "=", 0)]),
            ev([cmp(dist, "<", 280)], [
                setov("Murcielago", "cerca", "=", 1),
                I("AddForceXY", "Murcielago",
                  "(Lyra.CenterX() - Murcielago.CenterX()) / max(1, %s) * 150" % dist,
                  "(Lyra.CenterY() - Murcielago.CenterY()) / max(1, %s) * 150" % dist, 0)], [
                ev([ovar("Murcielago", "alerta", "=", 0)],
                   [sound("murcielago.wav", 45), setov("Murcielago", "alerta", "=", 1)]),
                ev([cmp("Lyra.CenterX()", "<", "Murcielago.CenterX()")], [flip("Murcielago", True)]),
                ev([cmp("Lyra.CenterX()", ">=", "Murcielago.CenterX()")], [flip("Murcielago", False)]),
            ]),
            ev([ovar("Murcielago", "cerca", "=", 0)], [
                setov("Murcielago", "alerta", "=", 0),
                I("AddForceXY", "Murcielago", "Murcielago.Variable(dir) * 80",
                  "(Murcielago.Variable(baseY) + sin(TimeFromStart() * 3 + Murcielago.Variable(minX)) * 30 - Murcielago.Y()) * 3", 0)], [
                ev([I("PosX", "Murcielago", "<=", "Murcielago.Variable(minX)")], [setov("Murcielago", "dir", "=", 1)]),
                ev([I("PosX", "Murcielago", ">=", "Murcielago.Variable(maxX)")], [setov("Murcielago", "dir", "=", -1)]),
                ev([ovar("Murcielago", "dir", "<", 0)], [flip("Murcielago", True)]),
                ev([ovar("Murcielago", "dir", ">", 0)], [flip("Murcielago", False)]),
            ]),
        ]),
    ], (52, 73, 94))

    ev_combate = group("Combate, daño y reaparición", [
        comment("Saltar sobre un enemigo lo derrota (rebote). Tocarlo de lado, o tocar pinchos, quita "
                "una vida y da 1,5 s de invulnerabilidad (Lyra parpadea)."),
        foreach("Enemigos", [
            ev([], [setn("Pisoton", "=", 0)]),
            ev([coll("Lyra", "Enemigos"), I("PlatformBehavior::IsFalling", "Lyra", "PlatformerObject"),
                cmp("Lyra.Y() + Lyra.Height()", "<", "Enemigos.CenterY() + 12")], [
                create("Humo", "Enemigos.CenterX() - 24", "Enemigos.CenterY() - 24"), delete("Enemigos"),
                setn("Pisoton", "=", 1), sound("aplastar.wav", 55),
                pb("JumpSpeed", "=", 520), pb("SetCanJump"), pb("SimulateJumpKey")]),
            comment("Pisoton evita que el enemigo recién eliminado cause daño en el mismo instante."),
            ev([num("Pisoton", "=", 0), coll("Lyra", "Enemigos")], [setn("Danio", "=", 1)]),
        ]),
        ev([num("Danio", "=", 1), timer("inv", ">=", "1.5")], [
            setn("Vidas", "-", 1), reset_timer("inv"), sound("golpe.wav", 60),
            pb("JumpSpeed", "=", 400), pb("SetCanJump"), pb("SimulateJumpKey")]),
        ev([], [setn("Danio", "=", 0)]),
        ev([timer("inv", "<", "1.5")], [opacity("Lyra", "=", "100 + mod(floor(TimeFromStart() * 14), 2) * 155")]),
        ev([timer("inv", ">=", "1.5")], [opacity("Lyra", "=", 255)]),
        comment("Caer al vacío: pierde una vida y reaparece en el último punto de control."),
        ev([I("PosY", "Lyra", ">", 620)], [
            setn("Vidas", "-", 1), sound("golpe.wav", 60), reset_timer("inv"),
            I("SetXY", "Lyra", "=", "Variable(CheckX)", "=", "Variable(CheckY)")]),
        ev([num("Vidas", "<=", 0)], [goto("GameOver")]),
    ], (192, 57, 43))

    ev_hudmsg = group("Interfaz (HUD) y mensajes", [
        ev([], [
            settext("TextoGemas", '"x " + ToString(GlobalVariable(Gemas))'),
            anim_expr("Vidas", '"v" + ToString(clamp(GlobalVariable(Vidas), 0, 3))'),
            I("SetX", "Mensaje", "=", "480 - Mensaje.Width() / 2"),
            I("SetX", "TextoNivel", "=", "940 - TextoNivel.Width()"),
        ]),
        ev([timer("msg", ">=", 3)], [settext("Mensaje", '""')]),
        ev([num("Dialogo", ">", 0)], [show("CajaDialogo"), show("TextoDialogo"), show("NombreDialogo"),
                                      show("TextoContinuar"), hide("IconoE")]),
        ev([num("Dialogo", "=", 0)], [hide("CajaDialogo"), hide("TextoDialogo"), hide("NombreDialogo"),
                                      hide("TextoContinuar")]),
        ev([], [setn("Accion", "=", 0)]),
    ], (127, 140, 141))

    head = [ev([], [hide("IconoE")])]
    return head, [ev_inicio, ev_controles, ev_anim, ev_camara], \
        [ev_items, ev_hongo, ev_goblin, ev_bat, ev_combate], ev_hudmsg


def anim_expr(o, expr):
    return I("AnimatableCapability::AnimatableBehavior::SetName", o, "Animation", "=", expr)


def dialogue_events(npc, nombre, lineas_por_tramo, cierre_extra):
    """Sistema de diálogo genérico.
    lineas_por_tramo: {indice_inicial: [lineas]} — cada tramo termina en indice_inicial+len.
    cierre_extra: {indice_inicial: [acciones al cerrar ese tramo]}"""
    evs = [
        comment("Diálogo: la variable Dialogo indica la línea que se muestra (0 = cerrado). "
                "E/Enter avanza; al terminar el tramo se cierra y se ejecutan sus consecuencias."),
        ev([num("Accion", "=", 1), num("Dialogo", ">", 0)], [setn("Dialogo", "+", 1), sound("dialogo.wav", 40)]),
    ]
    for start, lines in lineas_por_tramo.items():
        end = start + len(lines)
        evs.append(ev([num("Dialogo", "=", end)],
                      [setn("Dialogo", "=", 0), setn("Accion", "=", 0)] + cierre_extra.get(start, [])))
        for i, line in enumerate(lines):
            evs.append(ev([num("Dialogo", "=", start + i)], [settext("TextoDialogo", s(line))]))
    evs.append(ev([num("Dialogo", ">", 0)], [settext("NombreDialogo", s(nombre))]))
    evs.append(ev(near("Lyra", npc, 110, 100) + [num("Dialogo", "=", 0)], [
        show("IconoE"),
        I("SetXY", "IconoE", "=", "%s.CenterX() - 18" % npc, "=", "%s.Y() - 44 + sin(TimeFromStart() * 6) * 3" % npc)]))
    evs.append(ev([cmp("Lyra.CenterX()", "<", "%s.CenterX()" % npc)], [flip(npc, True)]))
    evs.append(ev([cmp("Lyra.CenterX()", ">=", "%s.CenterX()" % npc)], [flip(npc, False)]))
    return evs


# ---------------------------------------------------------------------- Nivel 1
def nivel1():
    sc = Scene("Nivel1")
    sc.variables = [var("Dialogo", 0), var("Accion", 0), var("Danio", 0), var("Pisoton", 0), var("TieneLlave", 0),
                    var("SabioHablo", 0), var("CheckX", 0), var("CheckY", 0), var("Saliendo", 0)]
    fondo(sc, "fondo_bosque", ["cielo", ("montanas", "Montanas"), ("arboles", "Arboles")])
    sc.objects += [
        tiled("SueloBosque", "suelo_bosque.png", [PLATFORM]),
        tiled("PlataformaMadera", "plataforma_madera.png", [JUMPTHRU]),
        sprite("Sabio", [("Quieto", ["sabio1.png", "sabio2.png"], 0.5, True)]),
        sprite("Cofre", [("cerrado", ["cofre_cerrado.png"], 0.1, False), ("abierto", ["cofre_abierto.png"], 0.1, False)]),
        sprite("Llave", [("Llave", ["llave.png"], 0.1, False)]),
        sprite("Portal", [("Remolino", ["portal%d.png" % i for i in range(1, 5)], 0.1, True)]),
        sprite("Arbusto", [("A", ["arbusto.png"], 0.1, False)]),
        sprite("Flor", [("F", ["flor.png"], 0.1, False)]),
    ]
    sc.groups = [{"name": "Enemigos", "objects": [{"name": "Goblin"}, {"name": "Murcielago"}]}]
    hud(sc, "Nivel 1 · Bosque de Sylvaria", True)

    ground(sc, "SueloBosque", [(0, 1104, GROUND), (1248, 768, GROUND), (2160, 528, 336),
                               (2832, 864, GROUND), (3888, 912, GROUND)])
    for (x, w, y) in [(720, 192, 312), (1488, 144, 216), (1728, 192, 168), (2016, 96, 384),
                      (2400, 144, 216), (3168, 192, 240), (3744, 96, 384), (4320, 144, 300)]:
        sc.inst("PlataformaMadera", x, y, w=w, h=24, z=6)
    for x in (1824, 3456):
        sc.inst("Pinchos", x, GROUND - 24, w=96, h=24, z=7)
    for (x, y) in [(60, 405), (530, 405), (980, 405), (1300, 405), (2300, 309), (2980, 405), (3990, 405), (4500, 405)]:
        sc.inst("Arbusto", x, y - 3, z=4)
    for x in (300, 640, 860, 1600, 2560, 3100, 3320, 4100, 4380, 4700):
        sc.inst("Flor", x, GROUND - 18, z=4)

    sc.inst("Lyra", 120, GROUND - 72, z=20)
    sc.inst("Sabio", 420, GROUND - 72, z=15)
    sc.inst("Cartel", 200, GROUND - 39, z=9,
            texto="← → o A/D para moverte · ESPACIO, ↑ o W para saltar · E para interactuar")
    sc.inst("Cartel", 1290, GROUND - 39, z=9, texto="¡Hongo mágico! Cae sobre él para impulsarte muy alto.")
    sc.inst("Cartel", 2900, GROUND - 39, z=9, texto="Dicen que un cofre antiguo descansa sobre las ramas altas...")
    sc.inst("Cartel", 4450, GROUND - 39, z=9, texto="Portal ancestral: solo se abre con la Llave Rúnica.")
    sc.inst("Hongo", 1392, GROUND - 42, z=9)
    sc.inst("Hongo", 3072, GROUND - 42, z=9)
    sc.inst("Bandera", 2232, 336 - 72, z=9)
    sc.inst("Cofre", 3240, 240 - 39, z=9)
    sc.inst("Portal", 4630, GROUND - 120, z=8)
    sc.inst("IconoE", -200, -200, z=30)

    for (x, mn, mx) in [(1620, 1470, 1740), (2960, 2860, 3400), (4000, 3910, 4380)]:
        sc.inst("Goblin", x, GROUND - 48, z=12, minX=mn, maxX=mx)
    sc.inst("Goblin", 2450, 336 - 48, z=12, minX=2360, maxX=2620)
    for (x, mn, mx, by) in [(2620, 2550, 2780, 190), (3550, 3300, 3700, 220), (4250, 4100, 4500, 200)]:
        sc.inst("Murcielago", x, by, z=12, minX=mn, maxX=mx, baseY=by)

    gems = [(560, 380), (620, 380), (680, 380), (790, 260), (850, 260), (1170, 300),
            (1530, 160), (1590, 160), (1780, 110), (1850, 110), (2060, 330), (2440, 160), (2500, 160),
            (2600, 280), (2760, 250), (2960, 380), (3220, 140), (3300, 140), (3780, 330),
            (3960, 380), (4100, 380), (4360, 250), (4420, 250)]
    for (x, y) in gems:
        sc.inst("Gema", x, y, z=9)
    sc.inst("Corazon", 1900, 120, z=9)
    sc.inst("Corazon", 3360, 190, z=9)

    head, pre, mid, post = common_level_events(sc, "musica_bosque.wav", "ambiente_bosque.wav",
                                               [("Montanas", "0.15"), ("Arboles", "0.4")], 1)
    sabio = group("NPC 3 · Sabio Eldric (diálogo y misión)", dialogue_events("Sabio", "Sabio Eldric", {
        1: ["¡Lyra, por fin llegas! El Rey Goblin Morgrak robó el Cristal del Alba\ny la oscuridad cubre todo Eldoria.",
            "Sin el Cristal, el sol no volverá a salir. Morgrak lo escondió\nen las Cavernas de Cristal, al otro lado del portal.",
            "El portal al final del bosque está sellado. Busca el cofre antiguo:\nguarda la Llave Rúnica que lo abre.",
            "Salta sobre los goblins para vencerlos. Y cuidado con los murciélagos:\nse lanzan en picada cuando te ven.",
            "Los hongos mágicos te impulsarán hacia lo alto.\n¡Que la luz de Eldoria te guíe!"],
        10: ["La Llave Rúnica está en un cofre sobre las ramas altas,\nmás allá del primer punto de control."],
        20: ["¡Tienes la Llave Rúnica! Corre hacia el portal, valiente Lyra."],
    }, {1: [setn("SabioHablo", "=", 1)] + message("Misión: encuentra la Llave Rúnica")}) + [
        ev([num("Accion", "=", 1), num("Dialogo", "=", 0)] + near("Lyra", "Sabio", 110, 100), [
            sound("dialogo.wav", 40), setn("Accion", "=", 0)], [
            ev([num("SabioHablo", "=", 0)], [setn("Dialogo", "=", 1)]),
            ev([num("SabioHablo", "=", 1), num("TieneLlave", "=", 0)], [setn("Dialogo", "=", 10)]),
            ev([num("SabioHablo", "=", 1), num("TieneLlave", "=", 1)], [setn("Dialogo", "=", 20)]),
        ]),
    ], (155, 89, 182))

    cofre = group("Entorno: cofre, llave y portal", [
        ev(near("Lyra", "Cofre", 80, 80) + [is_anim("Cofre", "cerrado"), num("Dialogo", "=", 0)], [
            show("IconoE"),
            I("SetXY", "IconoE", "=", "Cofre.CenterX() - 18", "=", "Cofre.Y() - 42 + sin(TimeFromStart() * 6) * 3")], [
            ev([num("Accion", "=", 1)], [
                anim("Cofre", "abierto"), sound("cofre.wav", 60), setn("Accion", "=", 0),
                create("Llave", "Cofre.CenterX() - 21", "Cofre.Y() - 40"),
                create("Destello", "Cofre.CenterX() - 18", "Cofre.Y() - 30")] + message("¡El cofre se abre!")),
        ]),
        ev([coll("Lyra", "Llave")], [
            delete("Llave"), setn("TieneLlave", "=", 1), show("IconoLlave"), sound("llave.wav", 60)]
           + message("¡Obtuviste la Llave Rúnica! El portal ya puede abrirse.")),
        ev([coll("Lyra", "Portal"), num("TieneLlave", "=", 0), ONCE],
           message("El portal está sellado. Necesitas la Llave Rúnica.")),
        ev([coll("Lyra", "Portal"), num("TieneLlave", "=", 1), num("Saliendo", "=", 0)], [
            setn("Saliendo", "=", 1), sound("portal.wav", 70), reset_timer("salida"), hide("Lyra"),
            create("Destello", "Lyra.CenterX() - 18", "Lyra.CenterY() - 18")]),
        ev([num("Saliendo", "=", 1), timer("salida", ">=", "1.6")], [goto("Transicion")]),
    ], (230, 126, 34))

    sc.events = head + pre + [sabio, cofre] + mid + [post]
    return sc


# ---------------------------------------------------------------------- Nivel 2
def nivel2():
    sc = Scene("Nivel2")
    sc.variables = [var("Dialogo", 0), var("Accion", 0), var("Danio", 0), var("Pisoton", 0), var("HadaHablo", 0),
                    var("CheckX", 0), var("CheckY", 0), var("Saliendo", 0), var("Abriendo", 0)]
    fondo(sc, "fondo_cueva", ["cielo", ("rocas", "Rocas"), ("cristales", "CristalesFondo")])
    sc.objects += [
        tiled("SueloCueva", "suelo_cueva.png", [PLATFORM]),
        tiled("PlataformaCristal", "plataforma_cristal.png", [JUMPTHRU]),
        sprite("PlataformaMovil", [("P", ["plataforma_movil.png"], 0.1, False)], [PLATFORM],
               variables=[("baseX", 0), ("rango", 140), ("vel", 1.2)]),
        sprite("Hada", [("Volar", ["hada1.png", "hada2.png"], 0.12, True)], variables=[("baseY", 0)]),
        sprite("Palanca", [("off", ["palanca_off.png"], 0.1, False), ("on", ["palanca_on.png"], 0.1, False)]),
        sprite("Compuerta", [("C", ["compuerta.png"], 0.1, False)], [PLATFORM]),
        sprite("Altar", [("Brillo", ["altar_cristal1.png", "altar_cristal2.png"], 0.4, True)]),
        sprite("Antorcha", [("Fuego", ["antorcha%d.png" % i for i in range(1, 4)], 0.12, True)]),
        sprite("Cristales", [("C", ["cristales.png"], 0.1, False)]),
    ]
    sc.groups = [{"name": "Enemigos", "objects": [{"name": "Goblin"}, {"name": "Murcielago"}]}]
    hud(sc, "Nivel 2 · Cavernas de Cristal", False)

    ground(sc, "SueloCueva", [(0, 912, GROUND), (1344, 1680, GROUND), (3456, 576, GROUND),
                              (4224, 576, GROUND)])
    for (x, w, y) in [(2208, 144, 336), (2400, 144, 240), (4080, 96, 384), (600, 144, 300),
                      (3650, 144, 300)]:
        sc.inst("PlataformaCristal", x, y, w=w, h=24, z=6)
    sc.inst("PlataformaMovil", 1060, 400, z=6, baseX=1060, rango=140, vel=1.2)
    sc.inst("PlataformaMovil", 3170, 400, z=6, baseX=3170, rango=140, vel=1.5)
    for x in (2592, 3850):
        sc.inst("Pinchos", x, GROUND - 24, w=96, h=24, z=7)
    for x in (120, 700, 1500, 2050, 2900, 3600, 4350, 4720):
        sc.inst("Antorcha", x, GROUND - 160, z=3)
    for x in (380, 820, 1700, 2300, 3520, 4280, 4500):
        sc.inst("Cristales", x, GROUND - 48, z=4)

    sc.inst("Lyra", 80, GROUND - 72, z=20)
    sc.inst("Hada", 330, 320, z=15, baseY=320)
    sc.inst("Cartel", 180, GROUND - 39, z=9, texto="Cavernas de Cristal. Habla con el hada Lumi (E).")
    sc.inst("Cartel", 2700, GROUND - 39, z=9, texto="La compuerta de Morgrak no se abre desde aquí... ¿una palanca?")
    sc.inst("Palanca", 2454, 240 - 36, z=9)
    sc.inst("Compuerta", 2784, GROUND - 144, z=8)
    sc.inst("Bandera", 3480, GROUND - 72, z=9)
    sc.inst("Hongo", 1950, GROUND - 42, z=9)
    sc.inst("Altar", 4620, GROUND - 102, z=8)
    sc.inst("IconoE", -200, -200, z=30)

    for (x, mn, mx) in [(1500, 1380, 1900), (2150, 2080, 2540), (3600, 3480, 3800), (3950, 3900, 4000),
                        (4350, 4240, 4560)]:
        sc.inst("Goblin", x, GROUND - 48, z=12, minX=mn, maxX=mx)
    for (x, mn, mx, by) in [(1200, 950, 1450, 210), (2600, 2380, 2760, 170), (3300, 3080, 3450, 220),
                            (4400, 4250, 4600, 200)]:
        sc.inst("Murcielago", x, by, z=12, minX=mn, maxX=mx, baseY=by)

    gems = [(520, 380), (640, 250), (700, 250), (1000, 320), (1120, 320), (1600, 380), (1700, 380),
            (2000, 200), (2250, 280), (2440, 180), (2520, 180), (2900, 380), (3100, 330), (3250, 330),
            (3560, 380), (3690, 250), (3750, 250), (4100, 330), (4300, 380), (4450, 380)]
    for (x, y) in gems:
        sc.inst("Gema", x, y, z=9)
    sc.inst("Corazon", 1980, 150, z=9)
    sc.inst("Corazon", 3720, 200, z=9)

    head, pre, mid, post = common_level_events(sc, "musica_cueva.wav", "ambiente_cueva.wav",
                                               [("Rocas", "0.2"), ("CristalesFondo", "0.45")], 2)
    curar = [setn("HadaHablo", "=", 1), setn("Vidas", "=", 3), sound("curar.wav", 60),
             create("Destello", "Lyra.CenterX() - 18", "Lyra.CenterY() - 18")] + message("Lumi restauró todas tus vidas")
    hada = group("NPC 4 · Hada Lumi (flota, guía y cura)", [
        ev([], [I("SetY", "Hada", "=", "Hada.Variable(baseY) + sin(TimeFromStart() * 2.5) * 8")]),
    ] + dialogue_events("Hada", "Hada Lumi", {
        1: ["¡Hola, Lyra! Soy Lumi, guardiana de estas cavernas.\nTe estaba esperando.",
            "Morgrak escondió el Cristal del Alba tras su compuerta de piedra.\nHay una palanca en lo alto que la abre.",
            "Los cristales flotantes se mueven: espera el momento justo para saltar.\nToma, deja que mi luz cure tus heridas."],
        10: ["Mi luz ya está contigo. ¡El Cristal del Alba te espera al final de la caverna!"],
    }, {1: curar}) + [
        ev([num("Accion", "=", 1), num("Dialogo", "=", 0)] + near("Lyra", "Hada", 110, 100), [
            sound("dialogo.wav", 40), setn("Accion", "=", 0)], [
            ev([num("HadaHablo", "=", 0)], [setn("Dialogo", "=", 1)]),
            ev([num("HadaHablo", "=", 1)], [setn("Dialogo", "=", 10)]),
        ]),
    ], (155, 89, 182))

    entorno = group("Entorno: plataformas móviles, palanca, compuerta y Cristal del Alba", [
        comment("Las plataformas móviles oscilan alrededor de baseX; el comportamiento Plataformero "
                "arrastra a Lyra cuando está encima."),
        foreach("PlataformaMovil", [
            ev([], [I("SetX", "PlataformaMovil", "=",
                      "PlataformaMovil.Variable(baseX) + sin(TimeFromStart() * PlataformaMovil.Variable(vel)) * PlataformaMovil.Variable(rango)")]),
        ]),
        ev(near("Lyra", "Palanca", 70, 70) + [is_anim("Palanca", "off"), num("Dialogo", "=", 0)], [
            show("IconoE"),
            I("SetXY", "IconoE", "=", "Palanca.CenterX() - 18", "=", "Palanca.Y() - 42 + sin(TimeFromStart() * 6) * 3")], [
            ev([num("Accion", "=", 1)], [
                anim("Palanca", "on"), sound("palanca.wav", 60), sound("puerta.wav", 70),
                setn("Abriendo", "=", 1), setn("Accion", "=", 0)] + message("¡Un estruendo! La compuerta de piedra se está abriendo...")),
        ]),
        ev([num("Abriendo", "=", 1)], [I("SetY", "Compuerta", "-", "90 * TimeDelta()")], [
            ev([I("PosY", "Compuerta", "<", 130)], [delete("Compuerta"), setn("Abriendo", "=", 2)]),
        ]),
        ev([coll("Lyra", "Altar"), num("Saliendo", "=", 0)], [
            setn("Saliendo", "=", 1), sound("curar.wav", 70), reset_timer("salida"),
            create("Destello", "Altar.CenterX() - 18", "Altar.Y()")]
           + message("¡Has recuperado el Cristal del Alba!")),
        ev([num("Saliendo", "=", 1), timer("salida", ">=", "2.2")], [goto("Final")]),
    ], (230, 126, 34))

    sc.events = head + pre + [hada, entorno] + mid + [post]
    return sc


# ---------------------------------------------------------------------- Menú
def menu():
    sc = Scene("Menu", (11, 10, 36))
    sc.layers = [""]
    sc.objects = [
        sprite("FondoMenu", [("F", ["fondo_menu.png"], 0.1, False)]),
        lyra_obj("LyraMenu", platformer=False),
        sprite("SabioMenu", [("Quieto", ["sabio1.png", "sabio2.png"], 0.5, True)]),
        text("Titulo", "Las Crónicas de Eldoria", 52, "255;216;74"),
        text("Subtitulo", "El Cristal del Alba", 28, "200;180;255"),
        text("Historia", "", 18, "235;235;255", bold=False),
        text("PulsaEnter", "Pulsa ENTER para comenzar", 26, "255;255;255"),
        text("Controles", "← → / A D: moverse    ESPACIO / ↑ / W: saltar    E / ENTER: interactuar", 16,
             "190;190;220", bold=False),
    ]
    # El fondo del menú es la portada (assets/portada/portada.png, de gen_portada.py), que ya trae
    # el título y los personajes; por eso Titulo, Historia, LyraMenu y SabioMenu no tienen instancias.
    sc.objects[0]["animations"][0]["directions"][0]["sprites"][0]["image"] = PORTADA
    sc.inst("FondoMenu", 0, 0, w=W, h=H, z=0)
    sc.inst("PulsaEnter", 330, 470, z=10)
    sc.inst("Controles", 200, 510, z=10)
    historia = ("Eldoria vivía en un amanecer eterno gracias al Cristal del Alba.\n"
                "Una noche, el Rey Goblin Morgrak lo robó y la oscuridad lo cubrió todo.\n"
                "Lyra, una joven exploradora del bosque, parte a recuperarlo.")
    sc.events = [
        ev([I("SceneJustBegins", "")], [music("musica_menu.wav"), settext("Historia", s(historia))]),
        ev([], [I("SetX", "Titulo", "=", "480 - Titulo.Width() / 2"),
                I("SetX", "Subtitulo", "=", "480 - Subtitulo.Width() / 2"),
                I("SetX", "Historia", "=", "480 - Historia.Width() / 2"),
                I("SetX", "PulsaEnter", "=", "480 - PulsaEnter.Width() / 2"),
                I("SetX", "Controles", "=", "480 - Controles.Width() / 2"),
                I("SetY", "Titulo", "=", "36 + sin(TimeFromStart() * 1.5) * 4")]),
        ev([cmp("mod(floor(TimeFromStart() * 2), 2)", "=", 0)], [show("PulsaEnter")]),
        ev([cmp("mod(floor(TimeFromStart() * 2), 2)", "=", 1)], [hide("PulsaEnter")]),
        ev([pressed_any("Return", "Space"), ONCE], [
            setn("Vidas", "=", 3), setn("Gemas", "=", 0), setn("NivelActual", "=", 1),
            sound("seleccionar.wav", 60), goto("Nivel1")]),
    ]
    return sc


# ---------------------------------------------------------------------- Cinemática de transición
def transicion():
    sc = Scene("Transicion", (11, 10, 36))
    sc.layers = ["", "Velo", "Titulo"]
    sc.objects = [
        sprite("FondoCine", [("F", ["fondo_cinematica.png"], 0.1, False)]),
        lyra_obj("LyraCine", platformer=False),
        sprite("PortalCine", [("Remolino", ["portal%d.png" % i for i in range(1, 5)], 0.08, True)]),
        sprite("MurcielagoCine", [("Volar", ["murcielago1.png", "murcielago2.png"], 0.12, True)]),
        text("Narracion", "", 22, "255;246;216"),
        text("TituloNivel", "NIVEL 2", 54, "255;216;74"),
        text("SubtituloNivel", "Las Cavernas de Cristal", 30, "200;180;255"),
        text("Saltar", "ENTER: saltar escena", 14, "160;160;190", bold=False, outline=False),
    ]
    sc.inst("FondoCine", 0, 0, z=0)
    sc.inst("PortalCine", 620, 330, z=4)
    sc.inst("LyraCine", -60, 378, z=5)
    for i, (x, y) in enumerate([(1000, 120), (1150, 180), (1300, 90)]):
        sc.inst("MurcielagoCine", x, y, z=6)
    sc.inst("Narracion", 60, 40, z=10)
    sc.inst("Saltar", 800, 515, z=10)
    sc.inst("Blanco", 0, 0, "Velo", W, H, z=1)
    sc.inst("Negro", 0, 0, "Velo", W, H, z=2)
    sc.inst("TituloNivel", 360, 200, "Titulo", z=1)
    sc.inst("SubtituloNivel", 300, 280, "Titulo", z=1)
    t = 'TimerElapsedTime("t")'
    linea1 = "Con la Llave Rúnica en la mano, Lyra cruzó el Bosque de Sylvaria..."
    linea2 = "El portal ancestral despertó y una luz violeta la envolvió por completo."
    sc.events = [
        comment("Escena animada de transición entre el Nivel 1 y el Nivel 2 (≈14 s), controlada por el "
                "temporizador «t»: fundido, Lyra corre hacia el portal, texto narrado letra a letra, "
                "destello blanco al cruzar y tarjeta de título del siguiente nivel."),
        ev([I("SceneJustBegins", "")], [
            music("musica_cinematica.wav", loop=False, vol=55), reset_timer("t"),
            opacity("Negro", "=", 255), opacity("Blanco", "=", 0), anim("LyraCine", "Correr"),
            hide("TituloNivel"), hide("SubtituloNivel")]),
        ev([timer("t", "<", 9)], [opacity("Negro", "=", "max(0, 255 - %s * 255)" % t)]),
        ev([I("PosX", "LyraCine", "<", 600), timer("t", "<", 6)], [I("AddForceXY", "LyraCine", 150, 0, 0)]),
        ev([I("PosX", "LyraCine", ">=", 600)], [anim("LyraCine", "Quieto")]),
        ev([], [I("AddForceXY", "MurcielagoCine", -170, "sin(TimeFromStart() * 4) * 40", 0),
                flip("MurcielagoCine", True)]),
        ev([timer("t", "<", 5)], [settext("Narracion", 'SubStr(%s, 0, floor(%s * 30))' % (s(linea1), t))]),
        ev([timer("t", ">=", 5), timer("t", "<", 9.5)],
           [settext("Narracion", 'SubStr(%s, 0, floor((%s - 5) * 30))' % (s(linea2), t))]),
        ev([timer("t", ">=", 6.5), ONCE], [sound("portal.wav", 70)]),
        ev([timer("t", ">=", 6.5), timer("t", "<", 7.6)],
           [opacity("Blanco", "=", "clamp((1 - abs(%s - 7) * 2) * 255, 0, 255)" % t)]),
        ev([timer("t", ">=", 7)], [hide("LyraCine")]),
        ev([timer("t", ">=", 7.6)], [opacity("Blanco", "=", 0)]),
        ev([timer("t", ">=", 9.5)], [opacity("Negro", "=", "min(255, (%s - 9.5) * 400)" % t),
                                     settext("Narracion", '""')]),
        ev([timer("t", ">=", 10.2)], [
            show("TituloNivel"), show("SubtituloNivel"),
            I("SetX", "TituloNivel", "=", "480 - TituloNivel.Width() / 2"),
            I("SetX", "SubtituloNivel", "=", "480 - SubtituloNivel.Width() / 2")]),
        ev([timer("t", ">=", 14)], [goto("Nivel2")]),
        ev([pressed_any("Return", "Space"), timer("t", ">", 1), ONCE], [goto("Nivel2")]),
    ]
    return sc


# ---------------------------------------------------------------------- Final y Game Over
def final():
    sc = Scene("Final")
    sc.layers = [""]
    sc.objects = [
        sprite("FondoFinal", [("F", ["fondo_final.png"], 0.1, False)]),
        lyra_obj("LyraFinal", platformer=False),
        sprite("CristalFinal", [("Brillo", ["altar_cristal1.png", "altar_cristal2.png"], 0.4, True)]),
        text("TextoFinal", "", 24, "255;255;255"),
        text("TextoVictoria", "¡VICTORIA!", 60, "255;216;74"),
        text("Volver", "Pulsa ENTER para volver al menú", 20, "40;30;60", outline=False),
    ]
    sc.inst("FondoFinal", 0, 0, z=0)
    sc.inst("LyraFinal", 380, 330, w=96, h=144, z=5)
    sc.inst("CristalFinal", 500, 330, w=96, h=136, z=5)
    sc.inst("TextoVictoria", 330, 40, z=10)
    sc.inst("TextoFinal", 120, 130, z=10)
    sc.inst("Volver", 330, 495, z=10)
    sc.events = [
        ev([I("SceneJustBegins", "")], [music("musica_final.wav", loop=False, vol=60),
                                        anim("LyraFinal", "Quieto")]),
        ev([], [
            settext("TextoFinal", s("Lyra devolvió el Cristal del Alba a su templo\ny el sol volvió a brillar sobre Eldoria.")
                    + ' + NewLine() + NewLine() + "Gemas recogidas: " + ToString(GlobalVariable(Gemas))'),
            I("SetX", "TextoFinal", "=", "480 - TextoFinal.Width() / 2"),
            I("SetX", "TextoVictoria", "=", "480 - TextoVictoria.Width() / 2"),
            I("SetX", "Volver", "=", "480 - Volver.Width() / 2"),
            I("SetY", "CristalFinal", "=", "320 + sin(TimeFromStart() * 2) * 6")]),
        ev([pressed_any("Return", "Space"), ONCE], [sound("seleccionar.wav", 60), goto("Menu")]),
    ]
    return sc


def gameover():
    sc = Scene("GameOver")
    sc.layers = [""]
    sc.objects = [
        sprite("FondoGameOver", [("F", ["fondo_gameover.png"], 0.1, False)]),
        text("TextoGameOver", "Fin del viaje...", 56, "255;90;110"),
        text("Reintentar", "ENTER: reintentar el nivel    ESC: menú principal", 20, "230;230;240"),
    ]
    sc.inst("FondoGameOver", 0, 0, z=0)
    sc.inst("TextoGameOver", 300, 190, z=10)
    sc.inst("Reintentar", 250, 300, z=10)
    sc.events = [
        ev([I("SceneJustBegins", "")], [music("musica_gameover.wav", loop=False, vol=60)]),
        ev([], [I("SetX", "TextoGameOver", "=", "480 - TextoGameOver.Width() / 2"),
                I("SetX", "Reintentar", "=", "480 - Reintentar.Width() / 2")]),
        ev([key("Return"), ONCE], [setn("Vidas", "=", 3), sound("seleccionar.wav", 60)], [
            ev([num("NivelActual", "=", 1)], [setn("Gemas", "=", 0), goto("Nivel1")]),
            ev([num("NivelActual", "=", 2)], [goto("Nivel2")]),
        ]),
        ev([key("Escape"), ONCE], [goto("Menu")]),
    ]
    return sc


# ====================================================================== Ensamblado
SHARED_BEHAVIORS = [
    {"name": "Animation", "type": "AnimatableCapability::AnimatableBehavior"},
    {"name": "Effect", "type": "EffectCapability::EffectBehavior"},
    {"name": "Flippable", "type": "FlippableCapability::FlippableBehavior"},
    {"name": "Opacity", "type": "OpacityCapability::OpacityBehavior"},
    {"name": "Platform", "type": "PlatformBehavior::PlatformBehavior"},
    {"name": "PlatformerObject", "type": "PlatformBehavior::PlatformerObjectBehavior"},
    {"name": "Resizable", "type": "ResizableCapability::ResizableBehavior"},
    {"name": "Scale", "type": "ScalableCapability::ScalableBehavior"},
    {"name": "Text", "type": "TextContainerCapability::TextContainerBehavior"},
]


def layer(name):
    return {"ambientLightColorB": 200, "ambientLightColorG": 200, "ambientLightColorR": 200,
            "camera2DPlaneMaxDrawingDistance": 5000, "camera3DFarPlaneDistance": 10000,
            "camera3DFieldOfView": 45, "camera3DNearPlaneDistance": 3, "cameraType": "",
            "followBaseLayerCamera": False, "isLightingLayer": False, "isLocked": False,
            "name": name, "renderingType": "", "visibility": True,
            "cameras": [{"defaultSize": True, "defaultViewport": True, "height": 0, "viewportBottom": 1,
                         "viewportLeft": 0, "viewportRight": 1, "viewportTop": 0, "width": 0}],
            "effects": []}


def layout_json(sc):
    return {
        "b": sc.color[2], "disableInputWhenNotFocused": True, "mangledName": sc.name, "name": sc.name,
        "r": sc.color[0], "standardSortMethod": True, "stopSoundsOnStartup": True, "title": "",
        "v": sc.color[1],
        "uiSettings": {"grid": False, "gridType": "rectangular", "gridWidth": 48, "gridHeight": 48,
                       "gridDepth": 48, "gridOffsetX": 0, "gridOffsetY": 0, "gridOffsetZ": 0,
                       "gridColor": 10401023, "gridAlpha": 0.8, "snap": False, "zoomFactor": 0.5,
                       "windowMask": False},
        "objectsGroups": sc.groups, "variables": sc.variables, "instances": sc.instances,
        "objects": sc.objects,
        "objectsFolderStructure": {"folderName": "__ROOT",
                                   "children": [{"objectName": o["name"]} for o in sc.objects]},
        "events": sc.events, "layers": [layer(l) for l in sc.layers],
        "behaviorsSharedData": SHARED_BEHAVIORS,
    }


def build():
    add_resources()
    gobjs = global_objects()
    scenes = [menu(), nivel1(), transicion(), nivel2(), final(), gameover()]
    project = {
        "firstLayout": "Menu",
        "gdVersion": {"build": 280, "major": 5, "minor": 6, "revision": 0},
        "properties": {
            "adaptGameResolutionAtRuntime": True, "antialiasingMode": "none",
            "antialisingEnabledOnMobile": False, "folderProject": False, "orientation": "landscape",
            "packageName": "com.eldoria.cronicas", "pixelsRounding": True,
            "projectUuid": "6f1d3c2e-8a4b-4f0e-9c1d-e1d0a1a2b3c4", "scaleMode": "nearest",
            "sizeOnStartupMode": "adaptWidth", "templateSlug": "",
            "useDeprecatedZeroAsDefaultStringVariable": False, "version": "1.0.0",
            "name": "Las Crónicas de Eldoria",
            "description": "Plataformas de fantasía: Lyra debe recuperar el Cristal del Alba robado por el Rey Goblin Morgrak.",
            "author": "", "windowWidth": W, "windowHeight": H, "latestCompilationDirectory": "",
            "maxFPS": 60, "minFPS": 20, "verticalSync": False, "platformSpecificAssets": {},
            "loadingScreen": {"backgroundColor": 0, "backgroundFadeInDuration": 0.2,
                              "backgroundImageResourceName": "", "gdevelopLogoStyle": "light",
                              "logoAndProgressFadeInDuration": 0.2, "logoAndProgressLogoFadeInDelay": 0.2,
                              "minDuration": 1.5, "progressBarColor": 16777215, "progressBarHeight": 20,
                              "progressBarMaxWidth": 200, "progressBarMinWidth": 40,
                              "progressBarWidthPercent": 30, "showGDevelopSplash": True,
                              "showProgressBar": True},
            "watermark": {"placement": "bottom-left", "showWatermark": True},
            "authorIds": [], "authorUsernames": [], "categories": ["adventure"],
            "playableDevices": ["keyboard"], "extensionProperties": [],
            "platforms": [{"name": "GDevelop JS platform"}], "currentPlatform": "GDevelop JS platform",
        },
        "resources": {"resources": resources, "resourceFolders": []},
        "objects": gobjs,
        "objectsFolderStructure": {"folderName": "__ROOT",
                                   "children": [{"objectName": o["name"]} for o in gobjs]},
        "objectsGroups": [],
        "variables": [var("Vidas", 3), var("Gemas", 0), var("NivelActual", 1)],
        "layouts": [layout_json(sc) for sc in scenes],
        "externalEvents": [], "eventsFunctionsExtensions": [], "externalLayouts": [],
    }
    with open(os.path.join(ROOT, "game.json"), "w", encoding="utf-8") as f:
        json.dump(project, f, ensure_ascii=False, indent=2)
    print("game.json generado: %d escenas, %d objetos globales, %d recursos"
          % (len(scenes), len(gobjs), len(resources)))


if __name__ == "__main__":
    build()
