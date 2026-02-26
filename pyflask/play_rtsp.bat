@echo off
REM ================================
REM 播放無人機 RTSP 串流 (ffplay)
REM ================================

REM 設定 RTSP URL
set RTSP_URL=rtsp://192.168.50.38:8554/live.sdp

REM 執行 ffplay
REM -fflags nobuffer : 盡量減少延遲
REM -rtsp_transport tcp : 用 TCP 避免 UDP 封包丟失
ffplay -fflags nobuffer -rtsp_transport tcp %RTSP_URL%
pause