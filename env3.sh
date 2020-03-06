export ROS_PYTHON_VERSION=3.7
export PYTHONPATH=$HOME/Library/Python/3.7/lib/python/site-packages

export PATH="/usr/local/opt/python/libexec/bin:/usr/local/opt/qt/bin:$PATH"
export CPPFLAGS="-I/usr/local/opt/qt/include -I/usr/local/opt/openssl@1.1/include -I/usr/local/opt/opencv@3/include -I/usr/local/include"
export LDFLAGS="-L/usr/local/opt/qt/lib -L/usr/local/opt/openssl@1.1/lib -L/usr/local/opt/opencv@3/lib -L/usr/local/lib"
export PKG_CONFIG_PATH="/usr/local/opt/qt/lib/pkgconfig:/usr/local/opt/openssl@1.1/lib/pkgconfig:/usr/local/opt/opencv@3/lib/pkgconfig"
export Boost_INCLUDE_DIR="/usr/local/opt/boost/include"
export OpenCV_DIR="/usr/local/opt/opencv@3/share/OpenCV"
export CMAKE_PREFIX_PATH="/usr/local/opt/opencv@3:/usr/local/opt/openssl@1.1:/usr/local/opt/qt"
