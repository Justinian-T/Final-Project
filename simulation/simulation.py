import mujoco
import numpy
import math
import mediapy as media

framerate = 30
data_rate = 100
width = 800
height = 600

# Define the XML template globally
xml_template = '''
<mujoco>
    <option>
        <flag gravity="enable" contact="enable" />
    </option>
    <option timestep="{ts:e}" />
    <compiler angle="degree" />
    <visual>
        <global offwidth="{width}" offheight="{height}" />
    </visual>

    <default>
        <geom contype="1" conaffinity="1" condim="3" friction="0.6 0.3 0.3" 
              solimp="0.99 0.99 0.01" solref="0.002 1" margin="0.001" />
    </default>

    <worldbody>
        <light name="top" pos="0 0 1" />
        <body name="floor" pos="0 0 0">
            <geom name="floor" pos="0 0 0" size="1 1 .05" type="plane" rgba="1 .83 .61 .5" />
        </body>
        <body name="trunk" pos="0 0 0">
            <joint name="joint1" type="slide" axis="0 0 1" />
            <geom name="trunk" pos="0 0.05 0.05" size=".025 .025 .025" type="box" rgba="1 1 0 1" mass=".01" contype="1" conaffinity="1"/>
            <body name="leg_link1" pos="-0.0125 0.05 0">
                <joint name="joint2" type="slide" axis="0 0 1" />
                <geom name="leg_link1" pos="0.025 0 0.015" size=".01 .01 .015" type="box" rgba="0.66 0 1 0.66" mass=".001" contype="1" conaffinity="1" />
                <body name="leg_link2" pos="0 0 0">
                    <joint name="joint3" type="hinge" axis="0 1 0" stiffness="{k:e}" damping="{b:e}" limited="true" range="0 90" />
                    <geom name="leg_link2" pos="{bsize2:e} 0 0" size="{bsize:e} 0.01 .01" type="box" rgba="1 0 0 1" mass=".001" />
                </body>
            </body>
        </body>
    </worldbody>

    <actuator>
        <motor name="motor1" joint="joint3" />
    </actuator>
</mujoco>
'''

def run_sim(k, b, grav, bsize, render=False):
    Vrom = 6
    R = Vrom / 0.6
    G = grav
    t_stall = 15 / 100 / G
    i_stall = 0.6
    i_nl = 0.2
    w_nl = 0.66 * 1000 * 2 * math.pi / 180 * G

    kt = t_stall / i_stall
    ke = kt

    b_calc = kt * i_nl / w_nl
    ts = 1e-4

    V_control = 5
    b_fit = 1.404e-6
    kp_fit = 8.896
    xml = xml_template.format(k=k, b=b, width=width, height=height, bsize=bsize, bsize2=bsize / 2, ts=ts)
    model = mujoco.MjModel.from_xml_string(xml)
    data = mujoco.MjData(model)
    renderer = mujoco.Renderer(model, width=width, height=height)

    # Set the initial angle of joint2 (in radians)
    def my_controller(model, data):
        w = data.qvel[1]  # Angular velocity of the joint
        actual = data.qpos[1]  # Current position of the joint
        trunk_velocity = data.qvel[0]  # Vertical velocity of the trunk

        # Define the desired position based on trunk motion
        if trunk_velocity < 0:  # Trunk is moving downward
            desired = 0  # Return to home position
        else:
            desired = math.pi  # Rotate to 180 degrees

        error = desired - actual
        V = kp_fit * error
        if V > V_control:
            V = V_control
        if V < -V_control:
            V = -V_control

        torque = (kt * (V - (ke) * w * G) / R - b_fit * w * G) * G

        data.ctrl[0] = torque

    try:
        mujoco.set_mjcb_control(my_controller)
        duration = 5

        frames = []
        t = []
        xy = []

        mujoco.mj_resetData(model, data)

        while data.time < duration:
            mujoco.mj_step(model, data)

            if render:
                if len(frames) < data.time * framerate:
                    renderer.update_scene(data)
                    pixels = renderer.render()
                    frames.append(pixels)

            if len(xy) < data.time * data_rate:
                t.append(data.time)
                xy.append(data.xpos.copy())

        if render:
            media.show_video(frames, fps=framerate, codec='gif')
        t = numpy.array(t)
        xy = numpy.array(xy)
    finally:
        mujoco.set_mjcb_control(None)

    return t, xy, frames