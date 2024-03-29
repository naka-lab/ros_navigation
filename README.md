# ros_navigation

## 準備
- リモートPC（各自のPC）で実行
    ```
    sudo -E apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --keyserver-option http-proxy=http://proxy.uec.ac.jp:8080 --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
    echo "export TURTLEBOT3_MODEL=burger" >> ~/.bashrc
    sudo apt-get install ros-noetic-turtlebot3-msgs
    sudo apt-get install ros-noetic-turtlebot3
    sudo apt-get install ros-noetic-dwa-local-planner
    sudo apt-get install ros-noetic-gmapping ros-noetic-map-server ros-noetic-find-object-2d
    cd ~/catkin_ws/src
    git clone https://github.com/naka-lab/ros_navigation.git
    source ~/.bashrc
    ```

- ロボット内部PCのIPの確認（nano ~/catkin_ws/set_ip.sh）
    ```
    export ROS_MASTER_URI=http://（リモートPCのIP）:11311
    export ROS_HOSTNAME=（ロボット内部PCのIP）
    ```

  - ロボット内部PC（raspberry pi）のユーザ名はpi，パスワードはturtlebot

- リモートPCのIPの確認（nano ~/catkin_ws/set_ip.sh）
    ```
    export ROS_MASTER_URI=http://（リモートPCのIP）:11311
    export ROS_HOSTNAME=（リモートPCのIP）
    ```


## 実行
- リモートPCで`roscore`を実行

### 地図生成（SLAM）
- ロボット内部PC（内部PCのデフォルトのユーザー名はpi, パスワードはturtlebot）
    ```
    roslaunch turtlebot3_bringup turtlebot3_robot.launch
    ```

- リモートPC
  - `roslaunch turtlebot3_slam turtlebot3_slam.launch`
  
  - `roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch`：起動したらキーボードを動かして地図を作成

  - `rosrun map_server map_saver -f ~/map`：地図を保存
  

### 地図の編集
- 編集ソフトを起動
  ```
  rosrun ros_navigation map_editor.py ~/map.yaml
  ```
- 画像上をドラッグして線を書いて編集する
  - 下側のスクロールバー：線の色（Color）と太さ（Size）の変更
  - `i`, `j`, `k`, `m`キー：地図のスクロール
  - `z`キー：元に戻す
  - `s`キー：保存
  - `q`キー：終了
- 編集が完了したら`s`キーを押すとファイル保存ダイアログが起動するのでファイル名を入力し保存
  
### ナビゲーション
- ロボット内部PC
    ```
    roslaunch turtlebot3_bringup turtlebot3_robot.launch 
    ```

- リモートPC：地図を指定して自己位置推定を実行
    ```
    roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/map.yaml
    ```

- rvizの「2D Pose Estimate」でロボットの現在位置を設定して，「2D Nav Goal」で移動先を指定する

- プログラムで座標指定で移動させる方法
  - [サンプル](https://github.com/naka-lab/ros_navigation/blob/main/scripts/navigation.py)参照
  - マップ上の座標の確認
  ```
  rosrun ros_navigation map_viewer.py ~/map.yaml
  ```
  
### 物体認識して追跡
- ロボット内部PC
    ```
    roslaunch turtlebot3_bringup turtlebot3_rpicamera.launch 
    roslaunch turtlebot3_bringup turtlebot3_robot.launch
    ```

- リモートPC  
  - 画像が圧縮されて来るので，それを復元してimage_rawという名前でpublishする
      ```
      rosrun image_transport republish compressed in:=/raspicam_node/image raw  out:=/image_raw
      ```
  - 物体認識ノード
      ```
      rosrun find_object_2d find_object_2d image:=/image_raw
      ```
  - `Edit`→`Add object from scene...`で認識したい物体を保存
  - [サンプル](https://github.com/naka-lab/ros_navigation/blob/main/scripts/object_tracking.py)を起動する  
