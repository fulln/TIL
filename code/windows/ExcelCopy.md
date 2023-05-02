#windows #excel

## 合并多个sheet

1. 打开excel

2. 打开函数

3. 粘贴

   ```shell
   Sub 合并当前工作簿下的所有工作表()
   Application.ScreenUpdating = False
   For j = 1 To Sheets.Count
     If Sheets(j).Name <> ActiveSheet.Name Then
         X = Range("A65536").End(xlUp).Row + 1
         Sheets(j).UsedRange.Copy Cells(X, 1)
     End If
   Next
   Range("B1").Select
   Application.ScreenUpdating = True
   MsgBox "当前工作簿下的全部工作表已经合并完毕！", vbInformation, "提示"
   End Sub
   ```

   

