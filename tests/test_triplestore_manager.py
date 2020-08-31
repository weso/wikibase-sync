from wbsync.triplestore import ModificationResult

def test_modification_result():
    msg = "Operation performed succesfully"
    res = ModificationResult(True, msg)
    assert res.successful
    assert res.message == msg
    assert res.result == ""
