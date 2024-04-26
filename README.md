Chỉ cần nhìn class Chess và class Piece + các class con, xử lý bàn cờ trên class Chess, field chess  
Hướng dẫn sử dụng Chess  
tạo 1 game chess= Chess()  
-> chess.chess = ma trận game  
chess.printChess() để in ma trận hiện tại  
Mặc định  
R_B K_B B_B Q_B K_B B_B K_B R_B  
P_B P_B P_B P_B P_B P_B P_B P_B  
\___  ___ ___ ___ ___ ___ ___ ___  
\___  ___ ___ ___ ___ ___ ___ ___  
\___  ___ ___ ___ ___ ___ ___ ___  
\___  ___ ___ ___ ___ ___ ___ ___  
P_W P_W P_W P_W P_W P_W P_W P_W  
R_W K_W B_W Q_W K_W B_W K_W R_W  
Gọi 1 quân cờ trong ma trận chess.chess[i][j] - cẩn thận None  
các quân cờ có 2 hàm cần quan tâm. Move(i,j) di chuyển đến vị trí i,j bất chấp điều kiện  
                                   possibleMove() trả về các vị trí có thể đi của quân cờ  
                                   -> Kết hợp 2 hàm trên để mô phỏng trò chơi  
Còn thiếu Nhập thành + Phong cấp
