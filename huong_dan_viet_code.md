# Hướng dẫn tự viết game "Escape from Blackwood Forest" từ đầu tới cuối

Mục tiêu: bạn gõ lại toàn bộ code theo từng bước, hiểu từng đoạn làm gì, và biết chỗ nào cần mở nguồn tham khảo để xem cú pháp.

Quy ước trong tài liệu này:

- **VIẾT**: đoạn này bạn tự gõ, không cần nguồn.
- **XEM NGUỒN**: đoạn này có cú pháp đặc thù, mở link ghi kèm, tìm đúng mục ghi kèm, nhìn ví dụ rồi viết theo. Chỉ copy *cách viết cú pháp*, không copy nguyên đoạn code của họ.

Tạo file mới tên `text_adventure_game.py`, mở bằng VS Code hoặc IDLE, rồi làm theo thứ tự dưới đây. Sau mỗi bước lớn nên chạy thử để bắt lỗi sớm.

---

## Bước 1. Import thư viện và hằng số

**VIẾT**

```python
import re
import json
from datetime import datetime

SAVE_FILE = "game_results.json"
```

Giải thích:

- `re`: thư viện biểu thức chính quy (regex), dùng để kiểm tra tên người chơi (yêu cầu 3 của đề).
- `json`: dùng để lưu dữ liệu ra file JSON (yêu cầu 9).
- `datetime`: chỉ để ghi giờ chơi vào file, không bắt buộc, có cũng đẹp hơn.
- `SAVE_FILE`: tên file lưu kết quả, đặt thành biến ở đầu để sau này muốn đổi tên file chỉ sửa một chỗ. Viết IN HOA vì là hằng số (quy ước Python).

---

## Bước 2. Dictionary OUTCOMES (ánh xạ kết quả)

**XEM NGUỒN**: https://www.w3schools.com/python/python_dictionaries.asp
Cuộn xuống mục **"Nested Dictionaries"** (dictionary lồng trong dictionary) và **"Accessing Items"** (truy cập phần tử bằng `ten_dict["key"]`). Đây là đúng kiểu cấu trúc ta dùng.

```python
OUTCOMES = {
    "treasure": {
        "title": "You found the lost treasure!",
        "message": "Inside the chest you find gold coins and an old map that\n"
                   "leads you straight out of the forest. Not a bad day after all.",
        "score": 100
    },
    "escaped": {
        "title": "You escaped the forest",
        "message": "You made it out tired, dirty but alive. Nobody at home is\n"
                   "going to believe this story.",
        "score": 70
    },
    "rescued": {
        "title": "Rescued by the rangers",
        "message": "Just before dark a ranger patrol finds you sitting by the\n"
                   "river. A bit embarrassing, but you are safe.",
        "score": 50
    },
    "lost": {
        "title": "Lost in the forest",
        "message": "You walk in circles for hours until it gets dark. The forest\n"
                   "keeps you for one more night...",
        "score": 20
    },
    "bear": {
        "title": "Eaten by a bear",
        "message": "The cave was not empty. The bear was faster than you.\n"
                   "Game over.",
        "score": 0
    },
    "drowned": {
        "title": "Swept away by the river",
        "message": "The current was a lot stronger than it looked.\n"
                   "Game over.",
        "score": 0
    }
}
```

Giải thích:

- Mỗi **key** bên ngoài (`"treasure"`, `"escaped"`...) là một kết thúc của game. Các hàm cốt truyện sẽ `return` đúng một trong 6 chữ này.
- Giá trị của mỗi key là một dictionary nhỏ có 3 phần: `title` (tiêu đề), `message` (lời kết), `score` (điểm).
- Hai chuỗi viết sát nhau trên hai dòng (`"...\n" "..."`) Python tự nối thành một chuỗi. `\n` là xuống dòng.
- Đây chính là "từ điển để lập bản đồ kết quả" trong yêu cầu 8 của đề.

Muốn code "của mình" hơn: đổi lời kể, đổi điểm số, thêm một kết thúc mới. Chỉ cần nhớ key nào thêm vào đây thì phải có hàm nào đó `return` key đó.

---

## Bước 3. Hàm display_title()

**VIẾT**

```python
def display_title():
    """Prints the welcome message and the instructions of the game."""
    print("=" * 50)
    print("        ESCAPE FROM BLACKWOOD FOREST")
    print("=" * 50)
    print("You wake up alone in the middle of a dark forest.")
    print("You don't remember how you got here. The only thing")
    print("you know is that you have to find a way out.")
    print()
    print("HOW TO PLAY:")
    print(" - Read each situation carefully.")
    print(" - Type the number of your choice and press Enter.")
    print(" - Every decision changes how the story ends.")
    print(" - Your result is saved to a file when the game ends.")
    print("=" * 50)
    print()
```

Giải thích:

- Dòng trong `"""..."""` ngay dưới `def` gọi là docstring, mô tả hàm làm gì. Giảng viên thích thấy cái này.
- `"=" * 50` in 50 dấu `=` liền nhau, cách nhanh để vẽ đường kẻ.
- `print()` không có gì bên trong = in một dòng trống.
- Đây là yêu cầu 1 của đề: hàm tên **đúng** là `display_title`, không được đổi tên.

---

## Bước 4. Hàm get_player_name() với regex

**XEM NGUỒN**: https://docs.python.org/3/library/re.html

Trong trang đó dùng Ctrl+F tìm 2 chỗ:

1. Mục **"Regular Expression Syntax"**: đọc ý nghĩa các ký hiệu `^`, `$`, `[...]`, `{m,n}`.
2. Mục **"re.match(pattern, string, flags=0)"**: xem cách gọi hàm. Điểm cần nhớ: `re.match` trả về một đối tượng Match nếu khớp, trả về `None` nếu không khớp. Vì `None` được coi là False trong `if`, nên viết `if re.match(...)` là đủ.

Nguồn phụ: sách Sweigart (2019), chương 7 "Pattern Matching with Regular Expressions", giải thích dễ hiểu hơn docs.

```python
def get_player_name():
    """Asks for a name or codename and checks it with a regular expression.
    Rules: 3 to 15 characters, has to start with a letter, and only
    letters, numbers and underscores are allowed."""
    pattern = r"^[A-Za-z][A-Za-z0-9_]{2,14}$"

    while True:
        name = input("Enter your name or codename: ").strip()
        if re.match(pattern, name):
            return name
        else:
            print("Invalid name. Use 3-15 characters, start with a letter")
            print("and only use letters, numbers or underscores.\n")
```

Giải thích pattern `^[A-Za-z][A-Za-z0-9_]{2,14}$` (đọc từ trái sang phải):

| Phần | Nghĩa |
|---|---|
| `r"..."` | chữ `r` trước dấu nháy = raw string, để Python không hiểu nhầm dấu `\` |
| `^` | bắt đầu chuỗi |
| `[A-Za-z]` | đúng 1 ký tự là chữ cái (hoa hoặc thường) |
| `[A-Za-z0-9_]{2,14}` | tiếp theo từ 2 đến 14 ký tự, mỗi ký tự là chữ, số hoặc gạch dưới |
| `$` | kết thúc chuỗi |

Tổng cộng tên dài 1 + (2 đến 14) = 3 đến 15 ký tự, bắt đầu bằng chữ.

Giải thích luồng:

- `while True:` lặp vô hạn, chỉ thoát khi gặp `return`.
- `.strip()` bỏ khoảng trắng đầu/cuối người dùng vô tình gõ.
- Khớp thì `return name` (thoát hàm luôn). Không khớp thì in lỗi và vòng lặp hỏi lại.

Đây là yêu cầu 3 của đề.

---

## Bước 5. Hàm get_choice() (hàm tiện ích)

**VIẾT**

```python
def get_choice(prompt, options):
    """Keeps asking until the player types one of the valid options.
    options is a tuple like ("1", "2", "3")."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in options:
            return choice
        print("Please type one of these: " + ", ".join(options))
```

Giải thích:

- Mỗi màn chơi đều cần hỏi người chơi và chỉ chấp nhận vài đáp án. Thay vì viết lại vòng lặp kiểm tra ở mọi màn, gom vào một hàm.
- `prompt`: câu hỏi hiện ra. `options`: một **tuple** các đáp án hợp lệ, ví dụ `("1", "2", "3")`. Tuple là "bộ" trong đề bài.
- `.lower()` đổi về chữ thường, để người chơi gõ `Y` hay `y` đều được.
- `choice in options` kiểm tra đáp án có nằm trong tuple không.
- `", ".join(options)` nối các phần tử tuple thành chuỗi `1, 2, 3` để in gợi ý.

---

## Bước 6. Hàm forest_path() (màn 1: trong rừng)

**VIẾT**

```python
def forest_path(decisions):
    """First part of the story. Returns the next scene or an ending."""
    print("\nYou stand up and look around. There are three ways to go:")
    print("  1) Follow the sound of running water")
    print("  2) Walk towards a dark cave in the hillside")
    print("  3) Push straight through the thick bushes")

    choice = get_choice("What do you do? (1/2/3): ", ("1", "2", "3"))

    if choice == "1":
        decisions.append("followed the sound of water")
        print("\nYou follow the sound and soon reach a fast flowing river.")
        return "river"
    elif choice == "2":
        decisions.append("went up to the cave")
        print("\nYou climb the hill and stop in front of the cave entrance.")
        print("It is pitch black inside and smells like wet fur.")
        return "cave"
    else:
        decisions.append("pushed through the bushes")
        print("\nThe bushes get thicker and thicker. Every tree looks the same.")
        return "lost"
```

Giải thích:

- Hàm nhận vào `decisions`, là **list** do `main()` tạo. List trong Python truyền theo tham chiếu, nên `decisions.append(...)` ở đây sẽ thêm thẳng vào list của `main()`. Đây là yêu cầu 6 (lưu quyết định vào list).
- `if / elif / else` xử lý 3 lựa chọn: yêu cầu 4.
- Giá trị `return` quyết định chuyện gì xảy ra tiếp: `"river"` và `"cave"` là tên màn tiếp theo, `"lost"` là một key trong `OUTCOMES` nên game kết thúc luôn.
- `\n` ở đầu chuỗi để cách một dòng trống cho dễ đọc.

Ba hàm `forest_path`, `cave_scene`, `river_scene` cộng lại là "ít nhất hai hàm bổ sung điều khiển cốt truyện" (yêu cầu 5).

---

## Bước 7. Hàm cave_scene() (màn 2: hang)

**VIẾT**

```python
def cave_scene(decisions, inventory):
    """Cave part of the story. Can end the game or send the player to the river."""
    print("\nWhat do you want to do at the cave?")
    print("  1) Walk straight into the dark")
    print("  2) Search around the entrance first")
    print("  3) Forget the cave and walk downhill")

    choice = get_choice("What do you do? (1/2/3): ", ("1", "2", "3"))

    if choice == "1":
        decisions.append("walked into the dark cave")
        print("\nYou take a few steps inside. Something big is breathing...")
        return "bear"

    elif choice == "2":
        decisions.append("searched the cave entrance")
        # a set is used for the inventory so an item can't be added twice
        inventory.add("rope")
        inventory.add("lantern")
        print("\nBehind a rock you find an old rope and a rusty lantern.")
        print("The lantern still works! Now you can see a bit inside the cave.")
        print("  1) Go deeper with the lantern")
        print("  2) Take the stuff and walk down to the river")

        choice = get_choice("What do you do? (1/2): ", ("1", "2"))

        if choice == "1":
            decisions.append("explored the cave with the lantern")
            print("\nWith the light you spot a huge bear sleeping in the corner.")
            print("You sneak past it very slowly... and find an old wooden chest.")
            return "treasure"
        else:
            decisions.append("took the items and left the cave")
            print("\nYou walk downhill with your new gear and reach a wide river.")
            return "river"

    else:
        decisions.append("skipped the cave")
        print("\nYou walk downhill and after a while you reach a wide river.")
        return "river"
```

Giải thích:

- Thêm tham số `inventory`, là một **set** (tập hợp) chứa đồ người chơi nhặt được. Set không cho phần tử trùng, nên dùng cho túi đồ rất hợp lý. `inventory.add("rope")` thêm dây thừng vào túi.
- Lựa chọn 2 có thêm một câu hỏi con bên trong (if lồng if). Biến `choice` được gán lại giá trị mới, hoàn toàn bình thường.
- Có 3 kết quả ra khỏi hàm: `"bear"` và `"treasure"` kết thúc game, `"river"` đưa sang màn sông.

---

## Bước 8. Hàm river_scene() (màn 3: sông)

**VIẾT**

```python
def river_scene(decisions, inventory):
    """River part of the story. Always ends the game."""
    print("\nThe river is wide and the water looks freezing. On the other")
    print("side you can see what looks like a hiking trail.")
    print("  1) Swim across")
    print("  2) Walk along the bank and look for a bridge")
    print("  3) Sit down and wait for help")

    choice = get_choice("What do you do? (1/2/3): ", ("1", "2", "3"))

    if choice == "1":
        decisions.append("tried to swim across the river")
        # the rope from the cave saves the player here
        if "rope" in inventory:
            print("\nYou tie the rope around a tree, pull yourself across and")
            print("follow the trail out of the forest.")
            return "escaped"
        else:
            print("\nHalfway across the current grabs your legs...")
            return "drowned"
    elif choice == "2":
        decisions.append("looked for a bridge")
        print("\nAfter twenty minutes you find an old wooden bridge. It creaks,")
        print("but it holds. The trail on the other side leads you out.")
        return "escaped"
    else:
        decisions.append("waited for help by the river")
        print("\nYou sit down by the river. Hours pass...")
        return "rescued"
```

Giải thích:

- `"rope" in inventory` kiểm tra trong set có dây thừng không. Nhờ vậy quyết định ở màn hang ảnh hưởng tới màn sông: có dây thì bơi qua sống, không có thì chết đuối. Đây là điểm làm game có chiều sâu, nên nhớ để giải thích với giảng viên.
- Hàm này luôn trả về một key kết thúc, không bao giờ trả về tên màn khác.

---

## Bước 9. Hàm show_results()

**VIẾT**

```python
def show_results(name, decisions, outcome_key):
    """Prints the ending, the list of decisions and the score."""
    result = OUTCOMES[outcome_key]

    print("\n" + "*" * 50)
    print("  " + result["title"].upper())
    print("*" * 50)
    print(result["message"])
    print()
    print(f"{name}, this is the path you took:")
    for number, decision in enumerate(decisions, start=1):
        print(f"  {number}. You {decision}")
    print(f"\nFinal score: {result['score']} / 100")
```

Giải thích:

- `OUTCOMES[outcome_key]` lấy dictionary nhỏ tương ứng với kết thúc, rồi `result["title"]`, `result["score"]` lấy từng phần. Đây là chỗ dictionary "lập bản đồ kết quả" phát huy tác dụng.
- `.upper()` đổi tiêu đề thành chữ in hoa.
- `f"..."` là f-string: biến đặt trong `{}` sẽ được chèn vào chuỗi.
- `for number, decision in enumerate(decisions, start=1)`: vòng **for** duyệt list quyết định, `enumerate` cho thêm số thứ tự bắt đầu từ 1. Đây là vòng for của yêu cầu 8.
- Trong f-string đã dùng nháy kép bên ngoài nên bên trong phải dùng nháy đơn: `result['score']`.

---

## Bước 10. Hàm save_game_data() với JSON

**XEM NGUỒN**: https://docs.python.org/3/library/json.html

Ctrl+F tìm 2 hàm:

1. **`json.dump(obj, fp, *, ... indent=None ...)`**: ghi đối tượng Python ra file. Đọc phần giải thích tham số `indent`: nếu đặt `indent=4` file sẽ được xuống dòng và thụt lề 4 khoảng trắng cho dễ đọc. Chú ý `dump` (ra file) khác với `dumps` (ra chuỗi).
2. **`json.load(fp)`**: đọc file JSON thành đối tượng Python. Cũng chú ý `load` khác `loads`.

Ngay đầu trang có mục ví dụ, nhìn thấy mẫu `json.dump(..., f)` và `json.load(f)` là đủ.

Nguồn phụ: sách Matthes (2023), chương 10 "Files and Exceptions", mục "Storing Data" dùng đúng mẫu "thử đọc file, nếu không có file (`FileNotFoundError`) thì tạo mới". Code dưới đây theo đúng ý tưởng đó.

```python
def save_game_data(player_data):
    """Adds the player's data to the JSON file. Creates the file if needed."""
    try:
        with open(SAVE_FILE, "r") as file:
            all_results = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # first time playing or the file is broken, start with an empty list
        all_results = []

    all_results.append(player_data)

    with open(SAVE_FILE, "w") as file:
        json.dump(all_results, file, indent=4)

    print(f"Your result was saved to {SAVE_FILE} ({len(all_results)} games saved in total)")
```

Giải thích từng khối:

- `try:` mở file ở chế độ đọc `"r"` và `json.load` toàn bộ nội dung cũ vào `all_results` (là một list các ván đã chơi).
- `except (FileNotFoundError, json.JSONDecodeError):` nếu file chưa tồn tại (lần chơi đầu) hoặc file bị hỏng, bắt đầu với list rỗng thay vì để chương trình sập.
- `with open(...) as file:` là cách mở file an toàn, Python tự đóng file khi hết khối `with`.
- `all_results.append(player_data)` thêm ván vừa chơi vào cuối list.
- Mở lại file ở chế độ ghi `"w"` (ghi đè) và `json.dump` cả list ra. Vì ghi đè toàn bộ list cũ + ván mới nên dữ liệu cũ không mất.
- `len(all_results)` đếm tổng số ván đã lưu.

Đây là yêu cầu 9 của đề.

---

## Bước 11. Hàm main()

**VIẾT**

```python
def main():
    """Controls the flow of the whole game."""
    display_title()
    name = get_player_name()

    games_played = 0
    play_again = "y"

    # the player can keep playing as long as they answer 'y'
    while play_again == "y":
        games_played += 1
        decisions = []      # every choice the player makes goes in here
        inventory = set()   # items the player picks up

        print(f"\n--- Game {games_played} --- Good luck, {name}! ---")

        scene = forest_path(decisions)

        if scene == "cave":
            scene = cave_scene(decisions, inventory)
        if scene == "river":
            scene = river_scene(decisions, inventory)

        # at this point 'scene' is one of the keys in OUTCOMES
        show_results(name, decisions, scene)

        player_data = {
            "name": name,
            "game_number": games_played,
            "decisions": decisions,
            "items_found": sorted(inventory),   # json can't store a set directly
            "outcome": OUTCOMES[scene]["title"],
            "score": OUTCOMES[scene]["score"],
            "played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_game_data(player_data)

        play_again = get_choice("\nDo you want to play again? (y/n): ", ("y", "n"))

    print(f"\nThanks for playing, {name}! You played {games_played} game(s). Goodbye!")
```

Giải thích luồng (đây là yêu cầu 2: `main()` điều khiển toàn bộ):

1. Gọi `display_title()` rồi `get_player_name()`. Tên hỏi một lần, chơi lại không phải nhập lại.
2. `play_again = "y"` để vòng `while` chạy được lần đầu. Vòng **while** này là yêu cầu 7 (cho phép chơi lại).
3. Mỗi ván tạo list `decisions = []` và set `inventory = set()` mới, để ván sau không dính dữ liệu ván trước.
4. `scene = forest_path(decisions)` chạy màn 1, nhận về tên màn tiếp hoặc key kết thúc.
5. Hai câu `if` tiếp theo: nếu đang ở `"cave"` thì chạy màn hang, kết quả gán lại vào `scene`. Sau đó nếu `scene` là `"river"` (từ màn 1 hoặc từ hang chuyển sang) thì chạy màn sông. Dùng 2 `if` riêng, không `elif`, để hang có thể dẫn tiếp ra sông trong cùng một ván.
6. Sau 2 `if`, `scene` chắc chắn là một key trong `OUTCOMES`, gọi `show_results`.
7. Gom dữ liệu ván vào dictionary `player_data`. Lưu ý `sorted(inventory)` đổi set thành list vì JSON không lưu được set.
8. `datetime.now().strftime(...)` lấy giờ hiện tại dạng chữ `2026-10-15 07:42:30`.
9. Hỏi chơi lại bằng `get_choice` với tuple `("y", "n")`. Gõ `n` thì điều kiện `while` sai, vòng lặp dừng, in lời chào.

---

## Bước 12. Dòng chạy chương trình

**VIẾT**

```python
if __name__ == "__main__":
    main()
```

Giải thích: khi chạy file trực tiếp (`python text_adventure_game.py`) thì `__name__` bằng `"__main__"` nên `main()` được gọi. Nếu file này được `import` từ file khác thì không tự chạy. Đây là cách viết chuẩn của Python, giảng viên nào cũng quen.

---

## Bước 13. Chạy thử và kiểm tra

Mở terminal trong thư mục chứa file, chạy:

```bash
python3 text_adventure_game.py
```

(Windows thì gõ `python` thay cho `python3`.)

Kiểm tra lần lượt:

| Thử | Gõ | Phải thấy |
|---|---|---|
| Tên sai | `12` rồi Enter | báo `Invalid name`, hỏi lại |
| Tên đúng | `Agent_K` | sang màn 1 |
| Lựa chọn sai | `9` | báo `Please type one of these: 1, 2, 3` |
| Đường 100 điểm | `2`, `2`, `1` | `YOU FOUND THE LOST TREASURE!` |
| Chơi lại | `y` rồi `1`, `2` | `YOU ESCAPED THE FOREST`, 70 điểm |
| Thoát | `n` | `Thanks for playing` |

Sau đó mở file `game_results.json` vừa được tạo cùng thư mục, phải thấy 2 ván, mỗi ván có `name`, `decisions`, `items_found`, `outcome`, `score`, `played_at`.

Lỗi hay gặp khi tự gõ:

- `IndentationError`: thụt lề sai, Python dùng đúng 4 khoảng trắng mỗi cấp.
- `NameError: name 'get_choice' is not defined`: gõ sai tên hàm hoặc hàm được gọi trước khi định nghĩa. Thực ra chỉ cần tất cả hàm nằm trên dòng `if __name__ == "__main__"` là được.
- `KeyError: 'rivr'`: một hàm `return` chữ không khớp key trong `OUTCOMES` hoặc không khớp chữ so sánh trong `main()`. Kiểm tra chính tả các chuỗi `"river"`, `"cave"`.
- Quên dấu `:` cuối dòng `def`, `if`, `while`, `for`.

---

## Bước 14. Làm file nộp .txt

Đề yêu cầu nộp file `.txt`. File `text_adventure_game_submission.txt` đã có sẵn, gồm:

1. Overview: giới thiệu game.
2. How the requirements are met: giải thích 9 yêu cầu được đáp ứng ở hàm nào, có trích dẫn trong bài kiểu APA, ví dụ `(Python Software Foundation, n.d.-b; Sweigart, 2019)`.
3. Source code: dán toàn bộ code.
4. Sample run: kết quả một lần chạy.
5. Content of game_results.json.
6. References: 5 nguồn theo APA.

Nếu bạn tự gõ lại code có sửa lời kể hoặc điểm số, nhớ cập nhật lại mục 3 (code), mục 4 (sample run) và mục 5 (JSON) cho khớp với bản chạy thật. Điền tên, khóa học, ngày ở 3 dòng đầu.

---

## Tóm tắt chỗ nào cần nguồn

| Bước | Nguồn cần mở | Tìm mục gì |
|---|---|---|
| 2 (OUTCOMES) | W3Schools Python Dictionaries | Nested Dictionaries, Accessing Items |
| 4 (regex) | docs.python.org re | Regular Expression Syntax, re.match |
| 4 (regex) | Sweigart 2019 | chương 7 |
| 10 (JSON) | docs.python.org json | json.dump (tham số indent), json.load |
| 10 (JSON) | Matthes 2023 | chương 10, mục Storing Data |

Tất cả bước còn lại là Python cơ bản (print, input, if/elif/else, while, for, list, tuple, set), tự viết không cần nguồn.
