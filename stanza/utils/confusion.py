def format_confusion(confusion, labels=None, hide_zeroes=False):
    """
    pretty print for confusion matrixes
    adapted from https://gist.github.com/zachguo/10296432

    The matrix should look like this:
      confusion[gold][pred]
    """
    if labels is None:
        labels = set(confusion.keys())
        for key in confusion.keys():
            labels = labels.union(confusion[key].keys())
        if 'O' in labels:
            labels.remove('O')
            labels = ['O'] + sorted(labels)
        else:
            labels = labels.sorted()

    columnwidth = max([len(x) for x in labels] + [5])  # 5 is value length
    empty_cell = " " * columnwidth

    fst_empty_cell = (columnwidth-3)//2 * " " + "t/p" + (columnwidth-3)//2 * " "

    if len(fst_empty_cell) < len(empty_cell):
        fst_empty_cell = " " * (len(empty_cell) - len(fst_empty_cell)) + fst_empty_cell
    # Print header
    header = "    " + fst_empty_cell + " "

    # If the numbers are all ints, no need to include the .0 at the end of each entry
    all_ints = True
    for i, label1 in enumerate(labels):
        for j, label2 in enumerate(labels):
            if not isinstance(confusion.get(label1, {}).get(label2, 0), int):
                all_ints = False
                break
        if not all_ints:
            break

    if all_ints:
        format_cell = lambda confusion_cell: "%{0}d".format(columnwidth) % confusion_cell
    else:
        format_cell = lambda confusion_cell: "%{0}.1f".format(columnwidth) % confusion_cell

    # make sure the columnwidth can handle long numbers
    for i, label1 in enumerate(labels):
        for j, label2 in enumerate(labels):
            cell = confusion.get(label1, {}).get(label2, 0)
            columnwidth = max(columnwidth, len(format_cell(cell)))

    for label in labels:
        header = header + "%{0}s ".format(columnwidth) % label
    text = [header]

    # Print rows
    for i, label1 in enumerate(labels):
        row = "    %{0}s ".format(columnwidth) % label1
        for j, label2 in enumerate(labels):
            confusion_cell = confusion.get(label1, {}).get(label2, 0)
            cell = format_cell(confusion_cell)
            if hide_zeroes:
                cell = cell if confusion_cell else empty_cell
            row = row + cell + " "
        text.append(row)
    return "\n".join(text)


