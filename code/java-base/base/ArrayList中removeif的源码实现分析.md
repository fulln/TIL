---
dg-publish: true
title: ArrayList中removeif的源码实现分析
createTime: 2024-03-03 17:31
tags:
  - java
  - datastruct
  - javabasic
  - arrayList
---
```java
public boolean removeIf(Predicate<? super E> filter) {
    Objects.requireNonNull(filter);
    int removeCount = 0;
    final BitSet removeSet = new BitSet(size);
    final int expectedModCount = modCount;
    final int size = this.size;
    for (int i=0; modCount == expectedModCount && i < size; i++) {
        @SuppressWarnings("unchecked")
        final E element = (E) elementData[i];
        if (filter.test(element)) {
            removeSet.set(i);
            removeCount++;
        }
    }
    if (modCount != expectedModCount) {
        throw new ConcurrentModificationException();
    }

    final boolean anyToRemove = removeCount > 0;
    if (anyToRemove) {
        final int newSize = size - removeCount;
        for (int i=0, j=0; (i < size) && (j < newSize); i++, j++) {
            i = removeSet.nextClearBit(i);
            elementData[j] = elementData[i];
        }
        for (int k=newSize; k < size; k++) {
            elementData[k] = null;  // Let gc do its work
        }
        this.size = newSize;
    }

    return anyToRemove;
}

```

## 主要步骤
- 首先，检查传入的 `Predicate` 参数是否为null，如果为null则抛出 `NullPointerException` 异常。
- 初始化一个整型变量 `removeCount` 用于记录符合条件的元素个数，初始化一个 `BitSet` 对象 `removeSet` 用于记录需要删除的元素的索引。
- 获取当前 `ArrayList` 的修改次数 `modCount`，以及当前列表的大小 `size`。
- 遍历列表中的每个元素，对每个元素应用 `filter` 条件：
    - 如果 `filter.test(element)` 返回true，表示当前元素符合条件，将该元素的索引添加到 `removeSet` 中，并增加 `removeCount`。
- 在遍历过程中，如果 `modCount` 发生变化，抛出 `ConcurrentModificationException` 异常，防止并发修改。
- 根据 `removeSet` 中记录的需要删除的元素的索引，重新调整列表中的元素位置，将符合条件的元素移除。
- 最后，更新列表的大小为新的大小，并返回是否有元素被删除的标志。

## bitSet在里面的作用
在 `ArrayList` 类中使用 `BitSet` 记录被删除元素的索引有以下几个优点：
1. **高效性能**：`BitSet` 是一个位向量，可以高效地表示大量的位信息。在 `removeIf` 方法中，使用 `BitSet` 记录需要删除的元素的索引，可以以极低的内存消耗和高效的速度进行标记和检查。
2. **节省空间**：由于 `BitSet` 是位向量，它只占用非常少的内存空间来表示大量的位信息。在 `removeIf` 方法中，如果直接使用数组或集合来记录被删除元素的索引，会占用更多的内存空间。
3. **方便操作**：`BitSet` 提供了方便的位操作方法，如 `set`、`clear`、`nextClearBit` 等，可以方便地对位进行标记、清除和查找。在 `removeIf` 方法中，使用 `BitSet` 可以方便地记录需要删除的元素的索引，并在遍历过程中进行操作。
4. **保持顺序**：使用 `BitSet` 记录被删除元素的索引可以保持元素在列表中的顺序。在 `removeIf` 方法中，根据 `BitSet` 中记录的索引重新调整元素位置，可以保持列表的顺序不变。

综上所述，使用 `BitSet` 记录被删除元素的索引在 `ArrayList` 类的 `removeIf` 方法中能够提供高效性能、节省空间、方便操作和保持顺序的优势。因此，`BitSet` 是一个合适的数据结构来处理需要删除元素的索引信息