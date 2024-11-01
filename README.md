# NFT CDP Project

Dự án này bao gồm một loạt các tập lệnh Python được thực thi theo thứ tự nhất định để thu thập, chuyển đổi, và phân tích dữ liệu liên quan đến các bộ sưu tập NFT. Các tệp thực thi sẽ lần lượt thực hiện các tác vụ từ việc thu thập dữ liệu đến việc phân tích và đổi tên trường dữ liệu trong bộ sưu tập của bạn. 

## Cấu trúc Dự án

Các tệp được sắp xếp theo thứ tự như sau:

1. **`collection/collectionOpensea.py`**  
   Thu thập dữ liệu từ OpenSea cho các bộ sưu tập NFT và lưu trữ chúng vào cơ sở dữ liệu MongoDB.

2. **`contract/transformContract.py`**  
   Chuyển đổi dữ liệu hợp đồng để chuẩn hóa các định dạng và cấu trúc của thông tin hợp đồng NFT.

3. **`floor/floorPriceGold.py`**  
   Truy xuất và phân tích giá sàn (floor price) của các bộ sưu tập và thực hiện các phép tính liên quan đến giá sàn chuẩn.

4. **`floor/priceChangeRate.py`**  
   Tính toán tỷ lệ thay đổi giá sàn theo thời gian.

5. **`volume/volumeGold.py`**  
   Thu thập và phân tích dữ liệu khối lượng giao dịch của các bộ sưu tập NFT.

6. **`volume/volumeChangeRate.py`**  
   Tính toán tỷ lệ thay đổi khối lượng giao dịch để đánh giá biến động.

7. **`option/numberOfSaleGold.py`**  
   Phân tích số lượng giao dịch của các bộ sưu tập NFT.

8. **`option/ownersChainbase.py`**  
   Truy xuất và xử lý thông tin về các chủ sở hữu từ Chainbase.

9. **`option/rankCollectionMC.py`**  
   Xếp hạng các bộ sưu tập dựa trên một số chỉ số chính.

10. **`option/renameFields.py`**  
    Đổi tên các trường dữ liệu để đồng nhất hóa thông tin trong cơ sở dữ liệu.

## Cách Sử Dụng

Dự án được khởi động bằng cách chạy tệp chính (`main.py`). Trước khi chạy `main.py`, hãy chắc chắn rằng các tham số trong `config.txt` đã được điều chỉnh theo yêu cầu của bạn.

### Cách chạy:

```bash
python main.py
