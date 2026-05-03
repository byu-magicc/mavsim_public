"""
mavsim: manage_viewers
    - Beard & McLain, PUP, 2012
    - Update history:
        3/11/2024 - RWB
        4/1/2024 - RWB
"""
import pyqtgraph as pg
from viewers.mav_viewer import MavViewer
from viewers.mav_path_viewer import MavAndPathViewer
from viewers.mav_waypoint_viewer import MAVAndWaypointViewer
from viewers.mav_world_viewer import MAVWorldViewer
from viewers.mav_viewer_camera import MAVWorldCameraViewer
from viewers.planner_viewer import PlannerViewer
from viewers.data_viewer import DataViewer
from viewers.sensor_viewer import SensorViewer
from viewers.camera_viewer import CameraViewer
from viewers.geolocation_viewer import GeolocationViewer
import parameters.simulation_parameters as SIM
from message_types.msg_state import MsgState
from message_types.msg_delta import MsgDelta
from message_types.msg_sensors import MsgSensors
from message_types.msg_path import MsgPath
from message_types.msg_waypoints import MsgWaypoints
from message_types.msg_world_map import MsgWorldMap

class ViewManager:
    def __init__(self,
                 mav: bool=False,
                 path: bool=False,
                 waypoint: bool=False,
                 planning: bool=False,
                 map: bool=False,
                 camera: bool=False,
                 sensors: bool=False,
                 geo: bool=False,
                 data: bool=False,
                 save_plots: bool=False,
                 video: bool=False,
                 video_name: str=[],
                 ):
        self.mav_flag = mav
        self.path_flag = path
        self.waypoint_flag = waypoint
        self.planning_flag = planning
        self.map_flag = map
        self.camera_flag = camera
        self.sensor_flag = sensors
        self.geo_flag = geo
        self.data_flag = data
        self.save_plots_flag = save_plots
        self.video_flag = video
        # initial pyqt application
        self.app = pg.QtWidgets.QApplication([])
        # initialize video
        if self.video_flag is True:
            from viewers.video_writer import VideoWriter
            self.video = VideoWriter(
                video_name=video_name,
                bounding_box=(0, 0, 750, 750),
                output_rate=SIM.ts_video)
        # initialize visualizers
        if self.camera_flag:
            self.camera_view = CameraViewer()
            self.mav_view = MAVWorldCameraViewer(app=self.app)
        elif self.map_flag:
            self.mav_view = MAVWorldViewer(app=self.app)
        elif self.waypoint_flag:
            self.mav_view = MAVAndWaypointViewer(app=self.app)
        elif self.path_flag:
            self.mav_view = MavAndPathViewer(app=self.app)
        elif self.mav_flag:
            self.mav_view = MavViewer(app=self.app)
        if self.planning_flag:
            self.planner_viewer = PlannerViewer(app=self.app)
        if self.data_flag:
            self.data_view = DataViewer(
                app=self.app,
                dt=SIM.ts_simulation,
                plot_period=SIM.ts_plot_refresh,
                data_recording_period=SIM.ts_plot_record_data,
                time_window_length=30)
        if self.sensor_flag:
            self.sensor_view = SensorViewer(
                app=self.app,
                dt=SIM.ts_simulation,
                plot_period=SIM.ts_plot_refresh,
                data_recording_period=SIM.ts_plot_record_data,
                time_window_length=30)
        if self.geo_flag:
            self.geo_viewer = GeolocationViewer(
                app=self.app,
                dt=SIM.ts_simulation,
                plot_period=SIM.ts_plot_refresh,
                data_recording_period=SIM.ts_plot_record_data,
                time_window_length=30)

    def update(self,
               sim_time: float,
               true_state: MsgState=None,
               estimated_state: MsgState=None,
               commanded_state: MsgState=None,
               delta: MsgDelta=None,
               measurements: MsgSensors=None,
               path: MsgPath=None,
               waypoints: MsgWaypoints=None,
               map: MsgWorldMap=None,
               target=None,
               camera=None,
               estimated_target=None,
               ):
        if self.camera_flag:
            self.camera_view.update(camera.getProjectedPoints())
            self.mav_view.update(true_state, target, path, waypoints, map)
        elif self.map_flag:
            self.mav_view.update(true_state, path, waypoints, map)
        elif self.waypoint_flag:
            self.mav_view.update(true_state, path, waypoints)
        elif self.path_flag:
            self.mav_view.update(true_state, path)
        elif self.mav_flag:
            self.mav_view.update(true_state)
        if self.data_flag:
            self.data_view.update(
                true_state,  # true states
                estimated_state,  # estimated states
                commanded_state,  # commanded states
                delta,  # inputs to aircraft
                )
        if self.sensor_flag:
            self.sensor_view.update(measurements)
        if self.geo_flag:
            self.geo_viewer.update(estimated_target, target)
        if self.video_flag is True:
            self.video.update(sim_time)
        self.app.processEvents()

    def update_planning_tree(self,
               waypoints: MsgWaypoints=None,
               map: MsgWorldMap=None,
               waypoints_not_smooth: MsgWaypoints=None,
               tree: MsgWaypoints=None,
               radius: float=0.):
        self.planner_viewer.draw_tree_and_map(
            map,
            tree,
            waypoints_not_smooth,
            waypoints,
            radius)

    def close(self, dataplot_name: str=[], sensorplot_name: str=[]):
        # Save an Image of the Plot
        if self.save_plots_flag:
            if self.data_flag:
                self.data_view.save_plot_image(dataplot_name)
            if self.sensor_flag:
                self.sensor_view.save_plot_image(sensorplot_name)
        if self.video_flag:
            self.video.close()
