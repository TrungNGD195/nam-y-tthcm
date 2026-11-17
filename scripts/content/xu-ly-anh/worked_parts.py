"""Teaching presentation: explicit source subparts and local symbol/method notes.

Numerical tables and matrices come from exercises/calculations, not a second answer key.
"""
from copy import deepcopy
import math


GUIDES={
 'hist':('I là ảnh đầu vào; (r,c) là hàng và cột; g là mức xám; h(g) là số pixel bằng g; N là tổng số pixel; # là phép đếm, Σ là phép cộng các giá trị.',
         'Lần lượt xét các mức xám, đếm số lần mỗi mức xuất hiện trong ảnh và ghi vào bảng. Cộng các tần suất để kiểm tra bằng số hàng nhân số cột.'),
 'transform':('g là mức xám cũ; f(g) là hàm đổi mức; s=f(g) là mức mới; h(g) và h′(s) là số pixel trước và sau biến đổi.',
              'Tính f(g) cho từng mức cũ. Những mức cũ cho cùng s được gộp bằng cách cộng tần suất, không cộng giá trị mức xám. Kiểm tra tổng số pixel không đổi.'),
 'smooth':('h(g) là tần suất gốc; h_s(g) là tần suất đã làm trơn; W là số mức trong cửa sổ, phải lẻ; j là độ lệch so với mức đang xét.',
           'Đặt cửa sổ quanh g, cộng W tần suất rồi chia cho W. Ngoài miền mức xám lấy h=0 và vẫn chia đúng W. Dịch sang mức kế tiếp, chỉ làm tròn ở kết quả theo yêu cầu đề.'),
 'equal':('h(i) là số pixel ở mức i; t(g) là số pixel có mức ≤g; N là tổng pixel; L là số mức xám; TB=N/L là số pixel trung bình mỗi mức; f(g) hoặc s(g) là mức mới; round là làm tròn gần nhất.',
          'Cộng dồn h để có t. Tính mức mới bằng đúng công thức giáo trình hoặc slide mà câu đang dùng, làm tròn rồi giới hạn mức khi công thức yêu cầu. Thay từng pixel theo bảng ánh xạ, không sửa lần lượt trên ảnh đã biến đổi.'),
 'diffuse':('I là mức xám gốc tại pixel; e_prev là sai số truyền từ pixel trước; u là mức sau bù sai số; θ là ngưỡng; b∈{0,255} là mức đầu ra; e=b−u là sai số truyền tiếp; N là tổng pixel.',
            'Đầu mỗi hàng đặt e_prev=0. Tại mỗi pixel, trừ sai số trước để có u, so sánh u với θ để chọn 0/255, tính e=b−u rồi chuyển e cho pixel kế tiếp cùng hàng. Không truyền sai số cuối hàng sang hàng mới.'),
 'huff-prob':('n_i là số lần khối i xuất hiện; N_b là tổng số khối 2×2; p_i=n_i/N_b là xác suất khối; H là entropy, đơn vị bit/khối; log₂ là logarithm cơ số 2.',
              'Quét theo hàng khối, mỗi khối 2×2 đọc trái sang phải rồi trên xuống dưới. Đếm từng mẫu khối và chia cho tổng số khối để có xác suất; chỉ cộng các mẫu có xác suất khác 0 khi tính entropy.'),
 'huff-tree':('w là trọng số của một nút, bằng tần suất hoặc tổng tần suất các lá thuộc nút; cha là nút mới, trái/phải là hai nút được ghép.',
              'Chọn hai nút nhỏ nhất, ghép thành cha có trọng số bằng tổng, đưa cha lại danh sách và lặp. Gán nhánh trái 0, phải 1; từ mã là các bit trên đường từ gốc đến lá. Khi hòa dùng quy tắc đã ghi tại bài.'),
 'huff-rate':('n₁,n₂ là số bit trước/sau mã; n_i là số lần ký hiệu i; ℓ_i là độ dài từ mã i; N_b là số khối; L là số bit trung bình mỗi khối; CR là tỷ lệ nén; RD là dư thừa tương đối; H là entropy; η là hiệu suất.',
              'Nhân số lần mỗi ký hiệu với độ dài từ mã rồi cộng để có n₂. Chia n₁ cho n₂ để có CR; tính L và H cùng đơn vị bit/khối trước khi lấy η=H/L. Chi phí bảng mã chỉ cộng nếu đề yêu cầu.'),
 'morph':('X hoặc A là ảnh nhị phân; B là các độ lệch tại ô SE bằng 1 tính từ gốc; p là vị trí đang xét; b là một độ lệch của B; E là ảnh co; D là ảnh giãn; ∧ là AND, ∨ là OR.',
           'Đặt gốc SE tại p, chỉ xét các ô SE bằng 1. Co cho 1 khi tất cả điểm tương ứng bằng 1; giãn theo hit cho 1 khi có ít nhất một điểm bằng 1. Ngoài khung lấy 0. Với SE bất đối xứng, giãn chuẩn xét X(p−b), khác hit trực tiếp X(p+b).'),
 'edge':('I là ảnh đầu vào; (r,c) là vị trí tâm; i,j∈{−1,0,1} là độ lệch trong cửa sổ; Hx,Hy,Hz là mặt nạ; Gx,Gy là đáp ứng hai hướng; ⊗ ở bài này là đặt tâm, nhân tương ứng rồi cộng, không lật mặt nạ.',
          'Lấy cửa sổ 3×3 quanh tâm, nhân từng pixel với đúng trọng số cùng ô của mặt nạ rồi cộng đủ chín tích. Dịch tâm qua toàn ảnh, ngoài khung lấy 0. Giữ đáp ứng âm; chỉ cộng có dấu hoặc lấy trị tuyệt đối theo đúng ý hỏi.'),
 'otsu':('h(i) là tần suất mức i; N là tổng pixel; t(g) là số pixel lớp ≤g; m(g) là trung bình lớp ≤g; μ là trung bình toàn ảnh; f(g) là tiêu chuẩn tương đương phương sai giữa hai lớp; θ là ngưỡng chọn.',
          'Tính N và μ, rồi với từng g cộng số pixel và tổng mức xám có trọng số của lớp ≤g. Tính m và f, bỏ ngưỡng làm một lớp rỗng. Ghi đủ nghiệm tối ưu; chỉ lấy trung bình nếu phân hoạch tương ứng vẫn đạt cực đại, nếu không phải chọn một nghiệm tối ưu.'),
 'iso':('h(g) là tần suất mức g; t là ngưỡng đang thử; μ₁,μ₂ là trung bình có trọng số của hai lớp ≤t và >t; n là chỉ số vòng lặp; t_n+1 là ngưỡng vòng sau.',
         'Tách histogram bằng ngưỡng hiện tại. Với mỗi lớp, lấy tổng g·h(g) chia tổng h(g), rồi lấy trung bình hai kết quả làm ngưỡng mới. Lặp tới khi ngưỡng/phân hoạch không đổi; chỉ làm tròn mỗi vòng khi đề quy định.'),
 'background':('N là tổng pixel; h(g) là tần suất; maxp là mức có tần suất nền lớn nhất; p% là tỷ lệ tích lũy yêu cầu; a là mức phân vị được chọn; P(a) là tỷ lệ tích lũy tới a; T là ngưỡng.',
                'Cộng dồn histogram, tính p%·N, xác định đỉnh maxp và chọn a theo đúng quy ước ≥ hoặc ≤ ghi tại bài. Lấy điểm đối xứng của a qua maxp bằng T=2maxp−a; kiểm tra giả thiết nền trội gần đối xứng.'),
 'triangle':('Điểm histogram đang xét là (x_g,y_g)=(g,h(g)); Δ có phương trình Ax+By+C=0; A,B,C là hệ số đường thẳng, không phải ma trận ảnh; d(g) là khoảng cách vuông góc.',
              'Nối đỉnh và cuối đuôi theo đề để lập phương trình Δ. Thay từng cặp (g,h(g)) vào tử số, lấy trị tuyệt đối rồi chia √(A²+B²). So sánh các khoảng cách và chọn mức g lớn nhất về khoảng cách, không phải mức xám lớn nhất.'),
 'lzw-encode':('D là từ điển ánh xạ chuỗi sang mã; w là chuỗi đang giữ; c là ký hiệu mới đọc; wc là nối chuỗi w với c; D[w] là mã của w.',
                'Nếu wc đã có trong từ điển thì mở rộng w thành wc. Nếu chưa có thì xuất mã của w, thêm wc bằng mã kế tiếp và đặt w=c. Đọc hết dữ liệu phải xuất nốt mã của w.'),
 'lzw-decode':('D là từ điển phía nhận; next là chỉ số mục sắp thêm; w là chuỗi giải ở lượt trước; entry là chuỗi giải từ mã hiện tại; first là lấy ký hiệu đầu; dấu + giữa chuỗi là phép nối.',
                'Giải mã đầu theo từ điển gốc. Với mỗi mã sau, đọc entry, xuất entry rồi thêm w+first(entry), cập nhật w=entry. Nếu mã chính là next chưa có, lấy entry=w+first(w); không tự đoán một mục bất kỳ.'),
 'rate':('n₁ là dung lượng trước mã; n₂ là dung lượng sau mã; CR=n₁/n₂. M,N là số hàng/cột; b_pixel là bit/pixel; N_mã là số từ mã xuất; b_mã là bit/từ mã nếu có trong công thức.',
          'Đếm dữ liệu đầu vào và số từ mã thực xuất. Nhân mỗi số lượng với đúng số bit một đơn vị rồi tính n₁/n₂. Dùng cùng đơn vị ở tử và mẫu; CR<1 nghĩa là dữ liệu nở.'),
 'point':('r là mức xám đầu vào; s là mức xám đầu ra; ảnh 8 bit có miền 0–255; γ là số mũ gamma khi có; ln là logarithm tự nhiên; min/max giới hạn kết quả vào miền cho phép.',
           'Với từng pixel, lấy r từ ảnh gốc, chọn đúng nhánh của hàm nếu có, thay r vào công thức rồi làm tròn theo đề. Mỗi phép biến đổi áp dụng riêng trên ảnh gốc, không dùng kết quả phép trước làm đầu vào phép sau.'),
 'weighted':('I là ảnh gốc; g(r,c) là pixel đầu ra tại tâm (r,c); h(i,j) là trọng số cửa sổ; i,j là độ lệch hàng/cột; I₀₀,I₀₁,… là các pixel quanh góc (0,0).',
              'Đặt tâm cửa sổ lên pixel cần tính. Nhân từng pixel lân cận với trọng số tương ứng rồi cộng. Trung bình có mọi trọng số 1/9; bộ trọng số phải chia tổng trọng số 16. Dùng đúng đệm 0 hoặc lặp rìa khi cửa sổ vượt khung.'),
 'median':('W là tập chín giá trị trong cửa sổ; I(q) là mức xám tại vị trí q; g_med là đầu ra trung vị; g_avg là đầu ra trung bình; median là phần tử giữa sau sắp xếp.',
            'Lấy chín giá trị từ ảnh gốc. Với trung vị, sắp tăng rồi chọn phần tử thứ năm; với trung bình, cộng đủ chín giá trị rồi chia 9. Dịch cửa sổ chỉ qua chín vị trí trong mà đề yêu cầu.'),
 'knear':('p là vị trí tâm; I(p) là mức tâm gốc; k là số giá trị được chọn; K là tập vị trí có mức xám gần mức tâm nhất; AV_k là trung bình của chúng; θ là ngưỡng chênh lệch; g(p) là kết quả.',
           'Tính khoảng cách |I(q)−I(p)| cho chín mẫu, chọn k mẫu gần nhất kể cả tâm, rồi lấy trung bình. So |I(p)−AV_k| với θ: không vượt ngưỡng thì giữ tâm, vượt mới thay. Mọi cửa sổ dùng ảnh gốc.'),
 'seven':('x_i là chín mẫu trong cửa sổ; x_(i) là mẫu thứ i sau sắp tăng; x̄ là trung bình; G là trung bình hình học; M là trung vị; P là điểm giữa; d=2 nghĩa là bỏ một mẫu nhỏ nhất và một mẫu lớn nhất.',
           'Liệt kê và sắp chín mẫu. Tính lần lượt tổng/9, căn bậc chín của tích, phần tử thứ năm, max, min, (max+min)/2; với alpha-trimmed bỏ hai cực trị rồi lấy trung bình bảy mẫu còn lại.'),
 'cmy':('R,G,B là ba kênh đỏ/lục/lam 8 bit; R_n,G_n,B_n là kênh đã chia 255; C,M,Y là lượng cyan/magenta/yellow chuẩn hóa trong [0,1].',
         'Chia từng kênh RGB 8 bit cho 255 rồi lấy 1 trừ kênh tương ứng. So sánh C,M,Y để nhận ra loại mực cần nhiều nhất; không lấy 1 trừ trực tiếp giá trị 0–255.'),
 'openclose':('A là ảnh nhị phân; B là SE; ⊖ là co; ⊕ là giãn; ∘ là mở; • là đóng; O,C lần lượt là kết quả mở/đóng; ⊆ là bao hàm.',
               'Với mở, co trước rồi giãn chính ảnh vừa co. Với đóng, giãn trước rồi co chính ảnh vừa giãn. Giữ cùng SE và quy ước ngoài khung; khi kiểm tra bao hàm, so từng vị trí 1 chứ không chỉ so tổng số điểm.'),
 'boundary':('A là ảnh đối tượng; s hoặc B_i là SE; E=A⊖s là ảnh co; Eᶜ là phần bù trong khung ảnh; β là biên trong; ∩ hoặc AND là phép giao; dấu \\ là hiệu hai tập.',
              'Tính ảnh co từ A. Đảo 0↔1 trong ảnh co để có phần bù rồi AND với A, hoặc trực tiếp giữ pixel thuộc A mà không thuộc ảnh co. Đếm số ô 1 của kết quả để được số điểm biên.'),
 'grow':('A là ảnh đối tượng hoặc đường biên theo đề; Aᶜ là phần bù; B là SE điều khiển liên thông; X₀ là hạt giống; X_k là tập sau vòng k; ⊕ là giãn, ∩ là giao.',
          'Khởi tạo X₀ đúng các hạt đã cho. Mỗi vòng giãn X trước, sau đó AND với Aᶜ để làm đầy hoặc với A để trích thành phần. Ghi các điểm mới, lặp đến X_k=X_k−1. Làm đầy kết thúc bằng A′=A∪X_k.'),
 'outside':('X_ngoài là toàn bộ nền ngoài lan được tới từ hạt ngoài; A_đầy là ảnh gồm đường biên và các vùng kín; số mũ c là phần bù trong khung ảnh.',
             'Lan từ nền ngoài bằng SE chữ thập với ràng buộc không vượt đường biên, tới khi ổn định. Đảo 0↔1 của tập nền ngoài đã tìm để giữ đường biên và toàn bộ vùng kín.'),
 'rlc':('N_run hoặc N_cặp là số loạt/cặp được xuất; n₁ là số bit gốc; n₂ là số bit sau mã; CR là tỷ lệ nén. Với mã ký tự, cả hai độ dài được đếm bằng số ký tự.',
         'Quét theo thứ tự nguồn, ghi từng loạt và độ dài theo đúng định dạng đề. Đếm số mục nhân chi phí mỗi mục rồi tính CR. Phân biệt loạt 0 trước bit 1, mã ký tự+số lần và cặp giá trị–độ dài; không trộn ba quy ước.'),
 'dct8':('P(x,y) là mức xám tại hàng x, cột y, chỉ số từ 0 đến 7; u,v là chỉ số tần số hàng/cột; T(u,v) là hệ số DCT; C(0)=1/√2, C(k>0)=1 là hệ số chuẩn hóa; π tính theo radian.',
          'Cố định u,v cần tìm, tính các trọng số cos theo x và y, nhân với P rồi cộng 64 pixel và nhân hệ số chuẩn hóa. Tận dụng các hàng giống nhau để rút gọn tổng, không tự trừ 128 khi đề yêu cầu bỏ dịch mức.'),
 'dc-recover':('T(0,0) là hệ số DC trực giao của khối 8×8; P̂ là ảnh tái tạo; P là ảnh gốc; e_rms là căn trung bình bình phương sai số trên 64 pixel.',
                'Đặt mọi hệ số AC bằng 0. DCT ngược khi chỉ còn DC cho mọi pixel bằng T(0,0)/8. Lấy từng sai lệch P−P̂, bình phương, cộng, chia 64 và lấy căn.'),
 'quant':('T hoặc I_DCT là hệ số DCT trước lượng tử; Q là bước lượng tử tại cùng ô, không phải số lượng màu; T′ hoặc I_Q là hệ số sau lượng tử; round là làm tròn gần nhất.',
           'Chia từng hệ số DCT cho đúng phần tử Q cùng vị trí rồi làm tròn nửa ra xa 0. Đây là phép chia từng phần tử, không phải phép chia ma trận. Đếm số ô khác 0 trên kết quả đã làm tròn.'),
 'ac':('AC là các hệ số ngoài DC; skip hoặc RUN là số hệ số 0 đứng trước một hệ số khác 0; value là hệ số đó; EOB=(0,0) báo đuôi toàn 0; ZRL=(15,0) biểu diễn 16 số 0.',
        'Đọc các AC theo zig-zag, đếm số 0 trước mỗi giá trị khác 0 rồi xuất cặp. Nếu đuôi còn toàn 0 thì kết thúc bằng EOB; không đưa DC vào dãy AC. Giải mã bằng chèn đúng số 0 trước mỗi value.'),
 'dequant':('T′ là hệ số lượng tử; Q là bảng bước lượng tử; T″ là hệ số khôi phục; ⊙ là nhân từng phần tử; SSE là tổng bình phương sai số hệ số; e_rms là sai số căn quân phương của khối 8×8.',
             'Nhân từng T′ với Q cùng ô để giải lượng tử. Lấy T−T″ ở mỗi ô, bình phương và cộng thành SSE; với DCT trực giao, chia SSE cho 64 rồi lấy căn để suy ra RMS trong miền ảnh.'),
 'dpcm':('DC_i là DC khối hiện tại; DC_i−1 là DC khối trước; d_i là hiệu cần mã; CAT là số bit biên độ. Với d=0 thì CAT=0; với d≠0 thì CAT=floor(log₂|d|)+1.',
          'Trừ DC khối trước khỏi DC hiện tại, khối đầu dùng DC trước mà đề cho. Tìm CAT từ độ lớn của hiệu. Tra mã Huffman của CAT rồi nối bit biên độ; số âm đảo các bit độ lớn trong CAT bit, không dùng bù hai.'),
 'dpcm-inverse':('DC_i−1 là DC đã khôi phục của khối trước; d_i là hiệu nhận được; DC_i là DC cần khôi phục.',
                  'Bắt đầu từ DC trước đã biết, cộng hiệu đầu để có DC đầu. Dùng chính kết quả mới làm DC trước cho lượt tiếp theo; lặp cộng dồn hết dãy.'),
 'dct2':('I là khối ảnh 2×2; T là ma trận DCT trực giao đề cho; Tᵀ là chuyển vị, đổi hàng thành cột; I_DCT là ma trận hệ số.',
          'Nhân T với I trước, rồi nhân kết quả với Tᵀ. Mỗi ô của tích lấy một hàng nhân một cột và cộng hai tích. Giữ dấu hệ số và chưa làm tròn trước bước lượng tử.'),
 'dc-bits':('DC là hệ số đầu vector zig-zag; DC_trước là hệ số của khối trước; d là hiệu DC; CAT là số bit biên độ; Huff(CAT) là từ mã tra bảng; dấu + giữa các bit là nối chuỗi.',
             'Lấy hiệu DC, xác định CAT, tra bảng Huffman cho CAT rồi nối bit biên độ. Dương dùng nhị phân độ lớn; âm dùng phần bù từng bit của độ lớn trong đúng CAT bit.'),
 'ac-bits':('RUN là số 0 trước value; CAT là số bit biểu diễn độ lớn value; Huff(RUN/CAT) là từ mã tra bảng AC; amplitude(value) là chuỗi bit biên độ, dấu + là nối chuỗi.',
             'Lập cặp RUN/value, tìm CAT của value, tra đúng hàng RUN/CAT rồi nối bit biên độ. Ghép các từ mã theo thứ tự quét và chỉ thêm EOB nếu còn đuôi 0.'),
 'inverse2':('Tᵀ là chuyển vị của ma trận DCT; I_Q là hệ số lượng tử; Q là bước lượng tử; ⊙ là nhân từng ô; I′ là ảnh tái tạo; e_rms là căn trung bình bình phương sai số trên bốn pixel.',
             'Nhân I_Q với Q từng ô, rồi tính Tᵀ·(I_Q⊙Q)·T. So từng pixel tái tạo với I gốc, bình phương sai lệch, cộng và chia 4 rồi lấy căn.'),
 'rms':('f là ảnh gốc, f̂ là ảnh giải nén ở cùng vị trí; SSE=Σ(f̂−f)² là tổng bình phương sai số; e_rms là căn trung bình bình phương sai số; 16 là số pixel của ảnh 4×4.',
         'Trừ hai ảnh từng ô, bình phương từng sai lệch rồi cộng thành SSE. Chia cho 16 và lấy căn; không lấy tổng sai lệch có dấu rồi mới bình phương.'),
 'snr':('f̂ là ảnh khôi phục; f là ảnh gốc; Σf̂² là năng lượng ảnh khôi phục theo quy ước slide; Σ(f̂−f)² là năng lượng sai số; SNR_ms là tỷ số, SNR_dB là giá trị decibel.',
         'Bình phương và cộng các pixel khôi phục để có tử số, chia cho SSE đã tính ở câu a. Đổi sang dB bằng 10log₁₀ của tỷ số, không lấy 20log₁₀ vì đây là tỷ số năng lượng.'),
 'prefix':('Từ mã là chuỗi bit ứng với một ký hiệu; mã tiền tố nghĩa là không từ mã nào là phần đầu của từ mã khác; gốc cây là nơi bắt đầu mỗi lượt đọc.',
            'Đọc từng bit, đi theo nhánh của cây; tới lá thì xuất một ký hiệu và trở lại gốc. Khi dựng ảnh, thay ký hiệu bằng đúng khối 2×2 rồi ghép theo hàng khối đề cho.'),
}


def family(s):
    f=s.get('formula','');lead=s['lead']
    if 'u=I-e_' in f:return 'diffuse'
    if 'm(g)=' in f and 'f(g)=' in f:return 'otsu'
    tests=[('hist',r'h(g)=\#'),('transform',"h'(s)="),('smooth','h_s(g)='),('equal','t(g)=\\sum'),
      ('diffuse','u=I-e_'),('huff-prob','p_i='),('huff-tree','w_{'),('huff-rate','n_2=\\sum'),
      ('morph','E(p)='),('edge','G_x(r,c)='),('edge','I_2(r,c)='),('iso',r'\mu_1(t)'),
      ('background','T=2'),('triangle','d(g)='),('lzw-decode',r'D[\mathrm{next}]'),
      ('point','s='),('weighted','g(r,c)='),('weighted','g_0('),('median','g_{med}'),('knear','AV_k='),
      ('seven',r'\begin{gathered}\bar x'),('cmy','R_n='),('openclose','B_1'),('openclose',r'A\circ'),
      ('openclose',r'A\bullet'),('openclose','O='),('boundary','E=A'),('boundary',r'\beta_i'),
      ('grow','X_k='),('outside','A_{'),('dct8','T(u,v)='),('dc-recover',r'\hat P'),
      ('quant',r'T^{\prime}(u,v)'),('ac',r'\mathrm{RLE}'),('ac',r'\mathrm{pair}'),
      ('dequant',r'T^{\prime\prime}'),('dpcm','d_i='),('dpcm-inverse','DC_i='),('dct2','I_{DCT}='),
      ('quant','I_Q='),('dc-bits','d=DC'),('ac-bits',r'\mathrm{bits}_{AC}'),('inverse2',r'I^{\prime}='),
      ('rms','e_{rms}='),('snr','SNR_{ms}='),('equal','p(r_k)='),('otsu','t(g)=')]
    if 'wc' in f and r'\notin' in f:return 'lzw-encode'
    if 'Từ mã' in f or 'Tu ma' in f:return 'prefix'
    for name,prefix in tests:
        if f.startswith(prefix):return name
    if 'N_{run}' in f or 'N_{cặp}' in f or 'số ký tự' in f:return 'rlc'
    if f.startswith('n_1=') or f.startswith('C_R='):return 'rate'
    if f:raise AssertionError('Missing symbol/method guide: '+lead+' '+f)
    return None


def annotate(s):
    if s.get('symbols') and s.get('method'):
        s.pop('_guide',None);return s
    name=s.pop('_guide',None) or family(s)
    if name:
        s.setdefault('symbols',GUIDES[name][0]);s.setdefault('method',GUIDES[name][1])
        if s.get('formula','').startswith('p(r_k)='):
            s['symbols']='r_k là mức xám thứ k; n_k là số pixel ở mức đó; p(r_k)=n_k/N là xác suất; N=32·32=1024; tổng tích lũy cộng từ mức 0 đến k; s_k là mức mới trong 0–7; round làm tròn gần nhất.'
    else:
        s.setdefault('method',s.get('text') or s.get('result') or s['lead'])
    return s


def take(s,**changes):
    result=deepcopy(s)
    for k,v in changes.items():
        if v is None:result.pop(k,None)
        else:result[k]=v
    return result


def label(steps,section):
    return [dict(s,section=section) for s in steps]


def plain(lead,text,**kw):return dict(lead=lead,text=text,**kw)


def ideal(s):
    return plain('Đối chiếu histogram với cân bằng lý tưởng.',
        'Ảnh cân bằng lý tưởng có cùng số pixel ở mọi mức xám. So từng cột của histogram kết quả, không chỉ kiểm tra tổng pixel. '+s['result'])


def edge_parts(s):
    """One directional response per step; the last operation combines the two."""
    blocks=s['blocks'];gx,gy,out=[b['rows'] for b in blocks]
    return [take(s,lead='Tính đáp ứng theo hướng x.',formula=s['formula'].split(r'\quad')[0].rstrip(','),blocks=[blocks[0]],result=None,ySubstitution=None),
      take(s,lead='Tính đáp ứng theo hướng y.',formula=s['formula'].split(r'\quad')[0].rstrip(',').replace('G_x','G_y').replace('H_x','H_y'),_guide='edge',
           substitution=s['ySubstitution'],blocks=[blocks[1]],result=None,ySubstitution=None),
      dict(lead='Ghép hai đáp ứng theo đúng yêu cầu đề.',formula='I_1=G_x+G_y' if 'cộng có dấu' in blocks[2]['caption'] else r'I_1=|G_x|+|G_y|',
           substitution=f'Tại (3,3), Gx={gx[2][2]}, Gy={gy[2][2]} ⇒ kết quả={out[2][2]}.',
           symbols='Gx,Gy là hai đáp ứng vừa tính tại cùng pixel; I₁ là kết quả ghép. Dấu | | là trị tuyệt đối khi có trong công thức.',
           method='Ghép từng cặp phần tử cùng vị trí. Cộng có dấu khi đề yêu cầu cộng hai ảnh; lấy trị tuyệt đối trước khi cộng khi đề yêu cầu độ lớn gradient. Không cắt giá trị âm ở giữa phép tính.',blocks=[blocks[2]])]


def morph_parts(s):
    b=s['blocks'];e,d=b[0]['rows'],b[1]['rows']
    co=take(s,lead='Tính ảnh co bằng điều kiện fit.',formula=r'E(p)=\bigwedge_{b\in B}X(p+b)',
        substitution=f'Tại (1,1), E={e[0][0]}; một ô ngoài ảnh bằng 0 đã đủ làm điều kiện AND sai.',blocks=b[:1],result=None,_guide='morph')
    di=take(s,lead='Tính ảnh giãn theo điều kiện hit của bộ bài.',formula=r'D_{hit}(p)=\bigvee_{b\in B}X(p+b)',
        substitution=f'Tại (1,1), D_hit={d[0][0]}; chỉ cần một vị trí SE hoạt động trùng pixel 1.',blocks=b[1:2],result=None,_guide='morph')
    extra=[]
    if len(b)>2:
        extra=[take(s,lead='Phản xạ SE để tính giãn theo định nghĩa tập hợp chuẩn.',
          formula=r'D_{std}(p)=\bigvee_{b\in B}X(p-b)',blocks=b[2:],
          substitution='Quay SE 180° quanh gốc rồi dò hit; kết quả chuẩn đặt riêng dưới đây, không thay thế phép hit trực tiếp ở câu trước.',result=None,_guide='morph')]
    return [co,di,*extra]


def diffuse_parts(s):
    b=s['blocks']
    a=take(s,blocks=[b[0],b[2]],result=None)
    comp=plain('So sánh khuếch tán lỗi với tách ngưỡng độc lập.',
      'Khuếch tán lỗi dùng để mô phỏng ảnh nhiều mức xám bằng các chấm đen–trắng trong in ấn. Bù sai số sang pixel sau thường giữ cảm nhận độ sáng vùng tốt hơn tách ngưỡng độc lập; không bảo toàn chính xác từng pixel.',
      formula=r'\bar I=\frac1N\sum_{r,c}I(r,c)',symbols='I(r,c) là mức tại pixel; N là tổng pixel; Ī là độ sáng trung bình. Pixel đen bằng 0, pixel trắng bằng 255.',
      method='Tách ngưỡng trực tiếp từng pixel ảnh gốc bằng cùng θ, không truyền sai số. Đếm số ô 255 của hai ảnh, rồi tính tổng mức xám chia tổng pixel để so với ảnh gốc.',
      substitution=s['result'],blocks=[b[1]])
    return [a,comp]


def organize(ident,original):
    s=deepcopy(original);groups=[]
    def add(section,*steps):groups.extend(label(steps,section))
    # Source labels are curated explicitly rather than guessed from text/OCR.
    if ident in ['bank-3-1','bank-3-2','uyen-3-T1','bank-3-3','uyen-5-T6']:
        add('Câu (a) — Biểu đồ tần suất',s[0]);add('Câu (b) — Biến đổi/làm trơn histogram',*s[1:3])
        if ident=='uyen-5-T6':add('Câu (c) — Đếm và nhận xét các đỉnh',s[3])
    elif ident in ['bank-3-4','bank-3-5','uyen-3-T3']:
        add('Câu (a) — Cân bằng theo giáo trình',s[0]);add('Câu (b) — Cân bằng lý tưởng',ideal(s[0]))
        if len(s)>1:add('Câu (c) — Công thức slide và so sánh',*s[1:])
    elif ident in ['bank-3-6','bank-3-7','uyen-4-T2','uyen-4-T3','uyen-4-T4']:
        a,b=diffuse_parts(s[0]);add('Câu (a) — Thực hiện khuếch tán lỗi',a);add('Câu (b) — Mục đích và so sánh',b)
    elif ident in ['bank-4-1','bank-4-2','uyen-5-T1','uyen-5-T2']:
        add('Câu (a) — Hai đáp ứng và ảnh I₁',*edge_parts(s[0]));add('Câu (b) — Đáp ứng Laplace I₂',s[1]);add('Câu (c) — Từ đáp ứng đến ảnh biên',s[2])
    elif ident in ['bank-4-3','bank-4-4','uyen-5-T3']:
        add('Câu (a) — Xử lý ảnh thứ nhất',*edge_parts(s[0]));add('Câu (b) — Xử lý ảnh thứ hai',*edge_parts(s[2]));add('Câu (c) — So sánh hai ảnh',s[4],s[1])
    elif ident in ['bank-4-5','bank-4-6','uyen-3-T10']:
        add('Câu (a) — Tìm ngưỡng và tách ảnh',*s)
        add('Câu (b) — Khi có nhiều ngưỡng cực đại',plain('Giữ đầy đủ các nghiệm trước khi chọn ngưỡng.',
          'Nhiều mức g có thể cùng đạt tiêu chuẩn lớn nhất, nhất là khi giữa hai nhóm mức xám có khoảng trống. Ghi đủ nghiệm tối ưu; chỉ dùng ngưỡng trung bình khi phân hoạch đó vẫn đạt cực đại. Nếu không, chọn một nghiệm tối ưu và công bố cách phá hòa. '+s[-1]['result']))
    elif ident in ['bank-4-7','bank-4-8','bank-4-8-bs']:
        add('Câu (a) — Đẳng điệu cho ảnh I',s[0]);add('Câu (b) — Đối xứng nền cho ảnh I′',s[1]);add('Câu (c) — Đánh giá và chọn phương pháp',*s[2:])
    elif ident=='bank-4-9':
        add('Câu (a) — Mã hóa và giải mã',*s);add('Câu (b) — Ý tưởng, hạn chế và xử lý',plain('Giải thích vì sao dùng từ điển thích nghi.',
          'LZW thay chuỗi lặp bằng mã từ điển; bên nhận tự tái tạo từ điển theo cùng quy tắc nên không phải gửi toàn bộ từ điển đã xây. Dữ liệu ngắn, ít lặp có thể nở; từ điển tăng làm tốn bộ nhớ và cần mã dài hơn. Khi đầy có thể ngừng thêm hoặc reset theo quy tắc đồng bộ giữa hai phía.'))
    elif ident=='uyen-3-T5':
        for title,indices in [('a',[0]),('b',[1]),('c',[2]),('d',[3]),('e',[4,5]),('f',[6,7])]:
            add(f'Câu ({title}) — '+{'a':'Tăng sáng','b':'Giảm sáng','c':'Âm bản','d':'Logarithm','e':'Hai giá trị gamma','f':'Kéo giãn và nhận xét'}[title],*[s[i] for i in indices])
    elif ident=='uyen-3-T6':
        add('Câu (a) — Tính tại tâm (2,2)',take(s[0],blocks=None))
        add('Câu (b) — Kết quả tại chín điểm trong',take(s[0],lead='Dịch cửa sổ tới từng điểm trong.',substitution='Lặp cách tính ở câu (a) cho hàng/cột 1–3, chỉ số từ 0; mỗi ma trận dưới đây có chín kết quả.',blocks=s[0]['blocks']))
        add('Câu (c) — Hai cách xử lý góc',s[1])
    elif ident=='uyen-3-T7':
        b=s[0]['blocks'];add('Câu (a) — Lọc trung vị',take(s[0],lead='Sắp chín mẫu và lấy phần tử thứ năm.',formula=r'g_{med}=\operatorname{median}(W)',substitution='Tại điểm trong đầu, dãy tăng là 0, 50, 50, 50, 51, 52, 52, 53, 255. Phần tử thứ năm là 51.',blocks=[b[1]],text=None,result=None))
        add('Câu (b) — Lọc trung bình',take(s[0],lead='Cộng chín mẫu rồi chia 9.',formula=r'g_{avg}=\frac19\sum_{q\in W}I(q)',blocks=[b[2]],text=None,result=None,_guide='median'))
        add('Câu (c) — Đối chiếu ảnh gốc và chọn bộ lọc',plain('So sánh từng vị trí cùng tọa độ.',s[0]['result'],blocks=[b[0]]))
    elif ident=='uyen-3-T9':
        add('Câu (a) — Tính bảy bộ lọc',take(s[0],text=None,result=None))
        add('Câu (b) — Nhận diện nhiễu và chọn bộ lọc',plain('Nhìn các giá trị đột biến so với nền.',s[0].get('text') or s[0].get('result','')))
    elif ident in ['uyen-3-T11','uyen-5-T5']:
        add('Câu (a) — Đẳng điệu ảnh A',s[0]);add('Câu (b) — Đối xứng nền ảnh B',s[1]);add('Câu (c) — Đổi chéo và nhận xét',*s[2:])
    elif ident=='uyen-5-T4':add('Câu (a) — Ngưỡng ảnh đã cho',s[0]);add('Câu (b) — Ví dụ nhiều ngưỡng cực đại',s[1])
    elif ident in ['bank-3-10','bank-3-11','uyen-7-T1','uyen-7-T2']:
        parts=morph_parts(s[0]);prefix='Câu (a)' if ident.startswith('uyen') else 'Phép tính'
        add(prefix+' — '+('Co và giãn ảnh' if ident.startswith('uyen') else 'Co ảnh'),parts[0])
        add(prefix+' — '+('Co và giãn ảnh' if ident.startswith('uyen') else 'Giãn ảnh'),parts[1])
        if len(parts)>2:add(('Câu (b)' if ident=='uyen-7-T2' else 'Đối chiếu quy ước')+' — SE phản xạ và giãn chuẩn',*parts[2:])
        elif ident=='uyen-7-T1':add('Câu (b) — Số điểm 1 và tác dụng',plain('Đếm và so sánh kích thước đối tượng.',s[0]['result']))
    elif ident=='uyen-7-T3':
        parts=morph_parts(s[0]);add('Câu (a) — Co với hai SE',parts[0],take(s[1],lead='Co với SE vuông B₂.',formula=r'E_2(p)=\bigwedge_{b\in B_2}X(p+b)',_guide='morph',text=None,result=None));add('Câu (b) — Giãn với SE chữ thập',parts[1]);add('Câu (c) — So sánh và chứng minh bao hàm',take(s[1],blocks=None))
    elif ident in ['uyen-7-T4','uyen-7-T5']:
        b=s[0]['blocks'];opening=ident.endswith('T4')
        add('Câu (a) — '+('Co' if opening else 'Giãn')+' trung gian',take(s[0],lead='Thực hiện phép đầu tiên trên ảnh gốc.',blocks=[b[0]],formula=r'E(p)=\bigwedge_{b\in B}A(p+b)' if opening else r'D(p)=\bigvee_{b\in B}A(p+b)',_guide='morph',result=None))
        add('Câu (b) — '+('Mở' if opening else 'Đóng')+' ảnh',take(s[0],blocks=[b[1]],result=None))
        add('Câu (c) — Giải thích các chi tiết thay đổi',plain('Đối chiếu ảnh đầu vào và kết quả.',s[0]['result']))
    elif ident=='uyen-7-T6':
        b=s[0]['blocks'];add('Câu (a) — Tính mở và đóng',take(s[0],blocks=b,result=None))
        add('Câu (b) — Kiểm tra bao hàm',plain('Kiểm tra ở từng pixel.', 'Mọi pixel 1 của O đều thuộc A; mọi pixel 1 của A đều thuộc C. Vì vậy O⊆A⊆C trên kết quả bài này; chỉ so số lượng pixel là chưa đủ chứng minh bao hàm.'))
        add('Câu (c) — Lặp lại và tính lũy đẳng',take(s[0],lead='Áp dụng lại cùng SE trên kết quả.',formula=r'O\circ B=O,\quad C\bullet B=C',_guide='openclose',blocks=[b[1],b[2]],result='Mở lần 2 bằng mở lần 1; đóng lần 2 bằng đóng lần 1. Đây là tính lũy đẳng.',text=None))
        add('Câu (d) — Vì sao mất phần bên trái',plain('Xét nơi có cửa sổ SE fit.','Phần bên trái'+s[0]['result'].split('Phần bên trái')[-1]))
    elif ident=='uyen-7-T7':
        for letter,title,formula,block in [('a','Ảnh co E',r'E=A\ominus s',s[0]['blocks'][0]),('b','Phần bù Eᶜ',r'E^c(r,c)=1-E(r,c)',s[0]['blocks'][1]),('c','Biên trong và số điểm',r'\beta(A)=A\cap E^c',s[0]['blocks'][2])]:
            explanation={'a':'Tại (hàng 2, cột 2), cả chín ô trong cửa sổ đều là 1 nên E(2,2)=1. Tại (1,1), cửa sổ có ô ngoài khung bằng 0 nên E(1,1)=0. Lặp cho các tâm còn lại.',
              'b':f'Tại ô đầu, E={s[0]["blocks"][0]["rows"][0][0]} ⇒ Eᶜ=1−E={block["rows"][0][0]}. Lặp phép đảo 0↔1 trên cả khung 6×10.',
              'c':s[0]['substitution']}[letter]
            method={'a':'Đặt gốc s lên từng pixel, lấy AND chín giá trị để được E.', 'b':'Giữ nguyên kích thước E, thay mỗi 0 bằng 1 và mỗi 1 bằng 0; không đảo cả miền ngoài ảnh.', 'c':'Lấy AND từng pixel của Eᶜ với A; chỉ các điểm thuộc A mà bị phép co xóa mới là biên.'}[letter]
            symbols={'a':'A là ảnh nhị phân đầu vào; s là SE vuông 3×3; ⊖ là phép co; E là ảnh co, cùng kích thước A.',
              'b':'E là ảnh co ở câu (a); Eᶜ là phần bù trong khung 6×10; (r,c) là tọa độ hàng/cột; 1−E đổi giá trị nhị phân 0↔1.',
              'c':'A là ảnh gốc; Eᶜ là phần bù vừa tính; β(A) là biên trong; ∩ hay AND chỉ cho 1 nếu cả hai pixel cùng bằng 1.'}[letter]
            add(f'Câu ({letter}) — {title}',take(s[0],lead={'a':'Co ảnh A với SE vuông 3×3.','b':'Lấy phần bù của ảnh co.','c':'Giao ảnh gốc với phần bù ảnh co.'}[letter],formula=formula,symbols=symbols,substitution=explanation,method=method,blocks=[block],_guide='boundary',result=s[0].get('result') if letter=='c' else None))
    elif ident=='uyen-7-T8':
        add('Câu (a) — Hai đường biên',s[0]);groups[-1].pop('result',None)
        add('Câu (b) — Khác biệt và liên thông',plain('So từng pixel rồi kiểm tra các điểm nối.',s[0]['result']))
    elif ident=='uyen-7-T9':
        a=take(s[0],blocks=s[0]['blocks'][:-1]);add('Câu (a) — Lặp lan hạt giống',a)
        add('Câu (b) — Hợp với đường biên',take(s[0],lead='Ghép phần trong với đường biên ban đầu.',formula=r"A'=A\cup X_k",blocks=s[0]['blocks'][-1:],substitution='Lấy OR từng pixel của ảnh A và X_k khi dừng; đường biên vẫn được giữ.',result=None,_guide='grow'))
        add('Câu (c) — Thay SE và chỉ ra chỗ rò',*s[1:])
    elif ident=='uyen-7-T10':add('Câu (a) — Hai hạt giống',s[0]);add('Câu (b) — Một hạt giống',s[1]);add('Câu (c) — Nền ngoài và cách tô toàn bộ',*s[2:])
    elif ident=='uyen-7-T11':
        for l,title,v in zip('abcd',['SE vuông, hạt (2,2)','SE chữ thập','Hạt (2,7)','Đếm thành phần'],s):add(f'Câu ({l}) — {title}',v)
    else:return finish_other(ident,s)
    return [annotate(v) for v in groups]


def finish_other(ident,s):
    # Compression has many source subparts; keep each numerical result with its own question.
    g=[]
    def add(title,*steps):g.extend(label(steps,title))
    if ident=='uyen-6-T1':
        rows=s[0]['blocks'][0]['rows'];nb=sum(r[1] for r in rows);n1=4*nb;n2=sum(r[1]*len(r[3]) for r in rows)
        entropy=-sum((r[1]/nb)*math.log2(r[1]/nb) for r in rows);avg=n2/nb
        freq=deepcopy(s[0]['blocks'][0]);freq['headers']=freq['headers'][:3];freq['rows']=[r[:3] for r in rows]
        add('Câu (a) — Tần suất khối',take(s[0],formula=r'p_i=n_i/N_b',blocks=[freq]))
        add('Câu (b) — Cây và bảng mã',take(s[1],blocks=[s[1]['blocks'][0],s[0]['blocks'][0]]))
        add('Câu (c) — Ma trận mã',plain('Thay từng khối bằng từ mã tương ứng.',
          'Mỗi ô của ma trận mã ứng với một khối 2×2 trong ảnh gốc. Quét hàng khối từ trái sang phải, trên xuống dưới; các từ mã có độ dài khác nhau.',
          method='Tra mẫu khối trong bảng mã câu (b), ghi nguyên chuỗi bit vào vị trí khối đó. Ví dụ mẫu '+str(rows[0][0])+' có mã '+str(rows[0][3])+'. Không cộng các bit thành một số.',blocks=s[1]['blocks'][1:]))
        add('Câu (d) — Số bit và tỷ lệ nén',take(s[2],formula=r'n_2=\sum_i n_i\ell_i,\quad C_R=n_1/n_2,\quad R_D=1-n_2/n_1',
          result=f'n₁={n1} bit; n₂={n2} bit; CR={n1/n2:.5f}; RD={1-n2/n1:.5f}. Chưa tính bảng mã.'))
        add('Câu (e) — Entropy và hiệu suất',take(s[2],lead='Tính entropy, độ dài trung bình và hiệu suất.',
          formula=r'H=-\sum_i p_i\log_2p_i,\quad L=n_2/N_b,\quad\eta=H/L',
          substitution='Các xác suất p_i: '+', '.join(str(round(r[2],5)) for r in rows)+f'; L={n2}/{nb}={avg:.5f}.',
          result=f'H={entropy:.5f} bit/khối; L={avg:.5f} bit/khối; η={entropy/avg:.5f}.',_guide='huff-rate'))
    elif ident=='uyen-6-T2':
        add('Câu (a) — Mã hóa Huffman và tỷ lệ nén',*s)
        add('Câu (b) — Đổi nhánh hoặc hòa tần suất',plain('Phân biệt chuỗi bit với tổng độ dài mã.',s[1]['result']))
        rows=s[0]['blocks'][0]['rows'];m=len(rows);nb=sum(r[1] for r in rows);fixed=math.ceil(math.log2(m));n1=nb*4;n2=nb*fixed
        add('Câu (c) — Mã độ dài cố định',plain('Chọn số bit đủ biểu diễn mọi mẫu khối.',
          'Mã cố định dùng cùng số bit cho mọi ký hiệu, không ưu tiên ký hiệu thường gặp như Huffman.',
          formula=r'b=\lceil\log_2 M\rceil,\quad n_2=N_b b,\quad C_R=n_1/n_2',
          symbols='M là số mẫu khối khác nhau; b là số bit mỗi khối; N_b là tổng số khối; n₁,n₂ là số bit trước/sau mã; ceil làm tròn lên.',
          method='Tìm số nguyên b nhỏ nhất sao cho 2^b≥M. Nhân b với số khối rồi so n₂ và CR với Huffman ở câu (a).',
          substitution=f'M={m}, b=ceil(log₂{m})={fixed}; n₂={nb}·{fixed}={n2}; CR={n1}/{n2}={n1/n2:.5f}.',
          result=f'Mã cố định: n₂={n2} bit, CR={n1/n2:.5f}; Huffman: n₂={sum(r[1]*len(r[3]) for r in rows)} bit, CR={n1/sum(r[1]*len(r[3]) for r in rows):.5f}. Huffman dùng ít bit hơn trong bài này.'))
    elif ident=='uyen-6-T3':
        add('Câu (a) — Tính tiền tố',plain('Kiểm tra không từ nào mở đầu từ khác.',s[0]['result']))
        add('Câu (b) — Giải mã và dựng ảnh',s[0]);add('Câu (c) — Tỷ lệ nén',s[1]);add('Câu (d) — Đảo bit và nhận xét',s[2])
    elif ident=='uyen-6-T4':
        add('Câu (a) — Mã hóa và giải mã',*s[:2]);add('Câu (b) — Số bit và tỷ lệ nén',s[2]);add('Câu (c) — Ý tưởng và hạn chế',plain('Nhận xét từ dãy mã và kích thước dữ liệu.',s[2]['result']+' Hai phía phải đồng bộ khi từ điển đầy; có thể ngừng thêm hoặc reset theo cùng quy tắc.'))
    elif ident=='uyen-6-T7':
        encoded,decoded=s[0]['result'].split(' Giải mã ',1)
        add('Câu (a) — Loạt 0 trước bit 1',take(s[0],result=encoded),plain('Giải mã từng nhóm bốn bit.',
          'Giải mã '+decoded,method='Đổi mỗi nhóm 4 bit thành số đếm thập phân k. Viết k số 0 rồi một số 1 cho mỗi nhóm trừ nhóm cuối; nhóm cuối chỉ ghi k số 0 tận cùng. Nối các đoạn theo thứ tự nhận.'))
        add('Câu (b) — Ký tự và số lần lặp',s[1]);add('Câu (c) — Cặp giá trị–độ dài',s[2])
    elif ident=='uyen-6-T8':
        add('Câu (a) — Hệ số DC T(0,0)',take(s[0],result=None))
        add('Câu (b) — Ba hệ số T(0,v)',take(s[0],lead='Thay u=0, lần lượt v=1,2,3.',substitution=s[0]['result'].split(' Các hàng')[0],result=None))
        add('Câu (c) — Các hệ số bằng 0',plain('Dùng tính trực giao của các hàm cos.','Các hàng'+s[0]['result'].split(' Các hàng')[1] if ' Các hàng' in s[0]['result'] else s[0]['result']))
        add('Câu (d) — Khôi phục chỉ bằng DC',s[1])
    elif ident=='uyen-6-T9':
        add('Câu (a) — Lượng tử hóa',take(s[0],result=None));add('Câu (b) — Đếm hệ số khác 0',plain('Đếm trên ma trận đã lượng tử.',s[0]['result'],method='Duyệt từng hàng của T′, đánh dấu các ô khác 0 rồi cộng số lượng. Đếm sau khi làm tròn, gồm cả DC, không đếm hệ số trước lượng tử hóa.'))
        add('Câu (c) — Vector zig-zag',take(s[1],lead='Quét chéo từ DC đến tần số cao.',formula=None,result=None,method='Bắt đầu (0,0), đi từng đường chéo và đảo hướng xen kẽ; đọc đủ 64 ô, không sắp xếp theo độ lớn hệ số.'))
        add('Câu (d) — RLE các AC',take(s[1],substitution=None));add('Câu (e) — Giải lượng tử và sai số',s[2])
    elif ident=='uyen-6-T10':
        add('Câu (a) — Dãy DPCM',take(s[0],formula=r'd_i=DC_i-DC_{i-1}',blocks=None,result=None))
        add('Câu (b) — CAT, bit biên độ và tổng bit',s[0]);add('Câu (c) — Khôi phục DC',s[1]);add('Câu (d) — Vì sao DPCM giảm bit',plain('So sánh độ lớn của hiệu với DC tuyệt đối.',s[1]['result']))
        add('Câu (e) — Mã hóa và giải mã AC',s[2])
    elif ident=='uyen-6-T11':
        add('Câu (a) — DCT',s[0]);add('Câu (b) — Lượng tử hóa',take(s[1],result=None))
        add('Câu (c) — Zig-zag',plain('Đọc theo thứ tự (0,0), (0,1), (1,0), (1,1).',s[1]['result'],method='Lấy lần lượt bốn ô từ I_Q theo thứ tự này, không tính lại DCT hoặc lượng tử hóa.'))
        add('Câu (d) — Mã DC',s[2]);add('Câu (e) — Mã AC và EOB',take(s[3],result=s[3]['result'].split('. ',1)[1]));add('Câu (f) — Chuỗi bit toàn khối',plain('Nối bit DC rồi bit AC theo thứ tự.',s[3]['result'].split('. ',1)[0]+'.',method='Lấy nguyên chuỗi DC ở câu (d), nối các từ mã AC ở câu (e). Đếm từng bit trong chuỗi kết quả, không cộng các giá trị nhị phân như số.'))
        dequant,restored,original=s[4]['blocks'];q=s[1]['blocks'][0]['rows'];dq=dequant['rows'];rec=restored['rows'];origin=original['rows']
        add('Câu (g) — Giải nén và RMS',dict(lead='Giải lượng tử hóa trước khi DCT ngược.',formula=r'\widehat I_{DCT}=I_Q\odot Q',
          symbols='I_Q là ma trận lượng tử ở câu (b); Q là bảng bước lượng tử của đề; ⊙ là nhân từng ô; Î_DCT là các hệ số khôi phục trước DCT ngược.',
          method='Nhân mỗi ô I_Q với đúng ô Q cùng hàng/cột; không nhân ma trận theo hàng–cột ở bước này. Hệ số đã làm tròn không tự khôi phục đúng hệ số DCT gốc.',
          substitution=f'Tại DC: {q[0][0]}·{dq[0][0]/q[0][0]:g}={dq[0][0]}; thu được ma trận dưới đây.',blocks=[dequant]),
          take(s[4],lead='Biến đổi DCT ngược để khôi phục ảnh.',formula=r"I'=T^T\widehat I_{DCT}T",
          symbols='T là ma trận DCT 2 điểm ở câu (a); Tᵀ là chuyển vị; Î_DCT là ma trận vừa giải lượng tử; I′ là ảnh khôi phục.',
          method='Nhân Tᵀ với ma trận hệ số đã giải lượng tử, rồi nhân kết quả với T. Với T của đề, ô (0,0) bằng tổng bốn hệ số chia 2.',
          substitution='I′(0,0)=('+' + '.join(str(x) for row in dq for x in row)+f')/2={rec[0][0]}. Các ô còn lại tính cùng quy tắc hàng nhân cột.',blocks=[restored]),
          dict(lead='Tính RMS từ bốn sai lệch pixel.',formula=r'e_{rms}=\sqrt{\frac14\sum_{r,c}(I(r,c)-I^{\prime}(r,c))^2}',
          symbols='I là ảnh gốc; I′ là ảnh khôi phục; (r,c) là vị trí pixel tương ứng; e_rms là căn trung bình bình phương sai số; 4 là số pixel của khối 2×2.',
          method='Trừ từng cặp pixel cùng vị trí, bình phương, cộng bốn số rồi chia 4 và lấy căn. Không lấy sai lệch có dấu trung bình vì chúng có thể triệt tiêu.',
          substitution='Các sai lệch: '+', '.join(f'{origin[r][c]}−{rec[r][c]}={origin[r][c]-rec[r][c]}' for r in range(2) for c in range(2))+'.',
          result='e_rms=√(('+ '+'.join(str((origin[r][c]-rec[r][c])**2) for r in range(2) for c in range(2))+')/4)='+str(round(math.sqrt(sum((origin[r][c]-rec[r][c])**2 for r in range(2) for c in range(2))/4),5))+'.',blocks=[original]))
    elif ident=='uyen-6-T12':
        for l,title,v in zip('abc',['Sai số RMS','Tỷ số SNR','Chất lượng và tỷ lệ nén'],s):add(f'Câu ({l}) — {title}',v)
    else:add('Bài giải',*s)
    return [annotate(v) for v in g]


def apply(solutions):
    for ident,value in solutions.items():value['steps']=organize(ident,value['steps'])
