# TurtleBot2 (kobuki) + Raspberry pi3(b+) 

## インストール
### Raspberry piのセットアップ
- raspberry pi 3 b+の場合はubuntu mate 18.04を使用
  - https://releases.ubuntu-mate.org/archived/18.04/arm64/
  - raspiのバージョンによって対応してるバージョンが違うので注意
- OSの時刻を設定（時刻がずれてると色々エラーになる）
- proxyを設定
- sshを設定
  ```
  sudo ssh-keygen -A
  sudo systemctl start ssh
  ```
- ROSインストールと環境設定
  ```
  sudo apt install curl

  # キーが古いので入れ替える
  sudo apt-key del F42ED6FBAB17C654
  sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --keyserver-option http-proxy=http://proxy.uec.ac.jp:8080 --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

  sudo apt update
  sudo apt install ros-melodic-desktop-full
  echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
  source ~/.bashrc

  source /opt/ros/melodic/setup.bash
  sudo apt install python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essential

  sudo -E rosdep init
  rosdep update
  source /opt/ros/indigo/setup.bash
  ```
  ```
  mkdir -p ~/catkin_ws/src
  cd ~/catkin_ws/src
  catkin_init_workspace
  cd ~/catkin_ws
  catkin_make
  echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
  echo "export ROS_MASTER_URI=http://127.0.0.1:11311" > ~/catkin_ws/set_ip.sh
  echo "export ROS_HOSTNAME=127.0.0.1" >> ~/catkin_ws/set_ip.sh
  echo "# ROSのIPは以下のファイルで切り替える" >>  ~/.bashrc
  echo "source ~/catkin_ws/set_ip.sh" >> ~/.bashrc
  source ~/.bashrc
  ls
  nano set_ip.sh
  source ~/.bashrc
  ```
- catkin_makeでメモリが足りなくなるのでswap領域を増やす
  ```
  sudo fallocate -l 2G /swapfile2
  sudo chmod 600 /swapfile2
  sudo mkswap /swapfile2
  sudo swapon /swapfile2
  swapon -s # swap領域が増えてるか確認
  ```
  
- turtlebot関係インストール
  ```
  sudo apt install python-catkin-tools
  cd catkin_ws
  curl -sLf https://raw.githubusercontent.com/gaunthan/Turtlebot2-On-Melodic/master/install_basic.sh | bash

  # ここで必要のなさそうなパッケージ（kobuki_gazebo_plugins，turtlebot_simulator）をcatkin_wsから移動させる

  catkin_make -j1 # メモリが足りなくなるのでスレッドを一つにする

  git clone https://github.com/ros-drivers/linux_peripheral_interfaces.git
  ```
  
- LRF関連インストール
  ```
  sudo apt install ros-melodic-urg-node
  ls /dev/tty* # ポートを確認する
  sudo chmod a+rw /dev/ttyACM0
  rosrun urg_node urg_node _serial_port:="/dev/ttyACM0" # 軌道を確認
  ```

- 独自プログラムをダウンロード
  ```
  cd ~/catkin_ws
  git clone https://github.com/naka-lab/ros_navigation.git
  ```

### リモートPCのセットアップ
```
cd ~/catkin_ws
git clone https://github.com/naka-lab/ros_navigation.git
```


## 準備
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
  roslaunch ros_navigation kobuki_minimal.launch 
  ```

- リモートPC
  - `roslaunch ros_navigation kobuki_slam.launch`
  - `roslaunch ros_navigation kobuki_teleop_key.launch`：起動したらキーボードを動かして地図を作成
  - `rosrun map_server map_saver -f ~/map`：地図を保存
  
### ナビゲーション
- ロボット内部PC
  ```
  roslaunch ros_navigation kobuki_minimal.launch 
  ```

- リモートPC：地図を指定して自己位置推定を実行
  ```
  roslaunch ros_navigation kobuki_navigaton.launch map_file:=$HOME/map.yaml
  ```

- rvizの「2D Pose Estimate」でロボットの現在位置を設定して，「2D Nav Goal」で移動先を指定する

- プログラムで座標指定で移動させる方法
  - [サンプル](https://github.com/naka-lab/ros_navigation/blob/main/scripts/navigation.py)参照
  - マップ上の座標の確認
  ```
  rosrun ros_navigation map_viewer.py ~/map.yaml
  ```
 
