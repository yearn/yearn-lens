import brownie


def test_filter_array(FilterArray, management):
    filterArray = FilterArray.deploy({"from": management})
    filteredArray = filterArray.removeZerosFromArray()
    print(f"Filtered array: {filteredArray}")
    assert len(filteredArray) == 3
