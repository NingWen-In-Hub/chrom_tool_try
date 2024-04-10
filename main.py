from collections import deque
import pandas as pd

class CaleRecioeStruct:
    def __init__(self, out_object, mul_num, div_num=1):
        self.out_object = out_object
        self.mul_num = mul_num
        self.div_num = div_num
        self.ifDel = False

    def __str__(self) -> str:
        return f"{self.out_object}\t*{self.mul_num}\t/{self.div_num}"
    
    def __eq__(self, other) -> bool:
        # print(other)
        return self.out_object == other.out_object


def find_index_by_val(queue, val):
    for i, item in enumerate(queue):
        if item.out_object == val:
            return i
    return -1  # 如果找不到符合条件的元素，则返回 -1

def gcd(a, b):
    # 最大公約数
    while b:
        a, b = b, a % b
    return a


def read_excel():
    # 读取Excel文件
    excel_file = pd.ExcelFile('RecipeBook.xlsx')

    # 读取第一个工作表的数据
    first_sheet_data = pd.read_excel(excel_file, sheet_name='目标配方', header=None)

    # 读取第二个工作表的数据
    second_sheet_data = pd.read_excel(excel_file, sheet_name='备用配方', header=None)

    # 打印第一个工作表的数据
    # print("First Sheet Data:")
    # print(first_sheet_data)

    # get end object
    end_object = first_sheet_data.at[0, 1]
    print(end_object)

    # get material dictionary
    material_dic = {}
    for index, row in first_sheet_data.iterrows():
        if index > 2:
            key = row[0]
            value = row[1]
            material_dic[key] = value

    print(material_dic)

    # 打印第二个工作表的数据
    # print("\nSecond Sheet Data:")
    # print(second_sheet_data)

    # get mediate dictionary
    medtiate_dic = {}
    temp_dic = {}
    for current_col in second_sheet_data.columns[::2]:
        if pd.isna(second_sheet_data.at[0, current_col+1]):
            break
        else:
            key = second_sheet_data.at[0, current_col+1]
            min_qua = second_sheet_data.at[1, current_col+1]
            if pd.isna(min_qua):
                print(f"レシピエラー：{key}の生産数が未設定　in (1, {current_col+1})")
                continue
            print(key)

            temp_dic.clear()
            for index, row in second_sheet_data.iterrows():
                if index > 2:
                    key_m = row[current_col]
                    if pd.isna(key_m):
                        continue
                    value_m = row[current_col + 1]
                    temp_dic[key_m] = value_m
            temp_dic['min_qua'] = min_qua
            print(temp_dic)
            medtiate_dic[key] = temp_dic.copy()
    print(medtiate_dic)
    return end_object, material_dic, medtiate_dic


def expand_recipe(end_object: str, material_dic: dict, medtiate_dic: dict):
    # レシピ展開
    # 创建一个空的双端队列
    queue_f = deque()
    queue_t = deque()
    waring_list = ""

    print("\n基本レシピ注入ing...")
    div_num = medtiate_dic[end_object].pop('min_qua')
    for recipe_t, num in medtiate_dic[end_object].items():
        tempCaleRecioeStruct = CaleRecioeStruct(recipe_t, num, div_num)
        queue_t.append(tempCaleRecioeStruct)
    for i in queue_t:
        print(i)

    print("\n基本レシピ処理開始")
    while len(queue_t) > 0:
        current_recipe: CaleRecioeStruct = queue_t.popleft()
        if current_recipe.out_object in material_dic.keys():
            index_t = find_index_by_val(queue_f, current_recipe.out_object)
            if index_t == -1:
                queue_f.append(current_recipe)
            else:
                tar_recipe: CaleRecioeStruct = queue_f[index_t]
                tar_recipe.mul_num = tar_recipe.mul_num*current_recipe.div_num + current_recipe.mul_num*tar_recipe.div_num
                tar_recipe.div_num = tar_recipe.div_num*current_recipe.div_num    
            print(f"queue更新")        
            for i in queue_f:
                print(i)

        elif current_recipe.out_object in medtiate_dic.keys():
            print(f"\n{current_recipe.out_object} 展開中")
            div_num = medtiate_dic[current_recipe.out_object]["min_qua"]
            for recipe_t, num in medtiate_dic[current_recipe.out_object].items():
                if recipe_t != "min_qua":
                    tempCaleRecioeStruct = CaleRecioeStruct(recipe_t, num * current_recipe.mul_num, current_recipe.div_num * div_num)
                    g_num = gcd(tempCaleRecioeStruct.mul_num, tempCaleRecioeStruct.div_num)
                    if g_num > 1:
                        tempCaleRecioeStruct.mul_num = tempCaleRecioeStruct.mul_num / g_num
                        tempCaleRecioeStruct.div_num = tempCaleRecioeStruct.div_num / g_num

                    queue_t.append(tempCaleRecioeStruct)
            print("臨時queue更新")
            for i in queue_t:
                print(i)

            print(f"{current_recipe.out_object} 展開完了\n")

        else:
            s_t = f"[warning]          {current_recipe.out_object}は対象外のため、注意！"
            waring_list += "\n"
            waring_list += s_t
            print(s_t)

    print("\n出力queue")
    for i in queue_f:
        i: CaleRecioeStruct
        g_num = gcd(i.mul_num, i.div_num)
        if g_num > 1:
            i.mul_num = i.mul_num / g_num
            i.div_num = i.div_num / g_num
        print(i)
    if len(waring_list) > 0:
        print(waring_list)

if __name__=="__main__":
    end_object, material_dic, medtiate_dic = read_excel()
    expand_recipe(end_object, material_dic, medtiate_dic)