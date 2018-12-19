import unittest
import bank_ocr


class TestBankOcr(unittest.TestCase):

    def test_one_account(self):
        self.assertEqual('111111111 ERR', bank_ocr.ocr('                           '
                                                       '  |  |  |  |  |  |  |  |  |'
                                                       '  |  |  |  |  |  |  |  |  |'
                                                       '                           '))
        self.assertEqual('222222222 ERR', bank_ocr.ocr(' _  _  _  _  _  _  _  _  _ '
                                                       ' _| _| _| _| _| _| _| _| _|'
                                                       '|_ |_ |_ |_ |_ |_ |_ |_ |_ '
                                                       '                           '))
        self.assertEqual('333333333 ERR', bank_ocr.ocr(' _  _  _  _  _  _  _  _  _ '
                                                       ' _| _| _| _| _| _| _| _| _|'
                                                       ' _| _| _| _| _| _| _| _| _|'
                                                       '                           '))
        self.assertEqual('444444444 ERR', bank_ocr.ocr('                           '
                                                       '|_||_||_||_||_||_||_||_||_|'
                                                       '  |  |  |  |  |  |  |  |  |'
                                                       '                           '))
        self.assertEqual('555555555 ERR', bank_ocr.ocr(' _  _  _  _  _  _  _  _  _ '
                                                       '|_ |_ |_ |_ |_ |_ |_ |_ |_ '
                                                       ' _| _| _| _| _| _| _| _| _|'
                                                       '                           '))
        self.assertEqual('666666666 ERR', bank_ocr.ocr(' _  _  _  _  _  _  _  _  _ '
                                                       '|_ |_ |_ |_ |_ |_ |_ |_ |_ '
                                                       '|_||_||_||_||_||_||_||_||_|'
                                                       '                           '))
        self.assertEqual('777777777 ERR', bank_ocr.ocr(' _  _  _  _  _  _  _  _  _ '
                                                       '  |  |  |  |  |  |  |  |  |'
                                                       '  |  |  |  |  |  |  |  |  |'
                                                       '                           '))
        self.assertEqual('888888888 ERR', bank_ocr.ocr(' _  _  _  _  _  _  _  _  _ '
                                                       '|_||_||_||_||_||_||_||_||_|'
                                                       '|_||_||_||_||_||_||_||_||_|'
                                                       '                           '))
        self.assertEqual('999999999 ERR', bank_ocr.ocr(' _  _  _  _  _  _  _  _  _ '
                                                       '|_||_||_||_||_||_||_||_||_|'
                                                       ' _| _| _| _| _| _| _| _| _|'
                                                       '                           '))
        self.assertEqual('123456789', bank_ocr.ocr('    _  _     _  _  _  _  _ '
                                                   '  | _| _||_||_ |_   ||_||_|'
                                                   '  ||_  _|  | _||_|  ||_| _|'
                                                   '                           '))

    def test_normal_account(self):
        self.assertEqual(bank_ocr.ocr(' _  _  _  _  _  _  _  _  _ '
                                      '| || || || || || || || || |'
                                      '|_||_||_||_||_||_||_||_||_|'
                                      '                           '), '000000000',)
        self.assertEqual(bank_ocr.ocr(' _  _  _  _  _  _  _  _    '
                                      '| || || || || || || ||_   |'
                                      '|_||_||_||_||_||_||_| _|  |'
                                      '                           '), '000000051')

    def test_ill_account(self):
        self.assertEqual(bank_ocr.ocr('    _  _  _  _  _  _     _ '
                                      '|_||_|| || ||_   |  |  | _ '
                                      '  | _||_||_||_|  |  |  | _|'
                                      '                           '), '49006771? ILL',)
        self.assertEqual(bank_ocr.ocr('    _  _     _  _  _  _  _ '
                                      '  | _| _||_| _ |_   ||_||_|'
                                      '  ||_  _|  | _||_|  ||_| _ '
                                      '                           '), '1234?678? ILL')

    def test_guess_digit(self):
        self.assertEqual(bank_ocr.guess_digit(' _ '
                                              ' _ '
                                              ' _|'), {'3', '5'})

        self.assertEqual(bank_ocr.guess_digit(' _ '
                                              '|_|'
                                              ' _ '), {'9'})

    def test_multi_account(self):
        self.assertEqual(bank_ocr.guess_multi_accounts('./accounts.txt'),
                         "711111111\n"
                         "777777177\n"
                         "200800000\n"
                         "333393333\n"
                         "888888888 AMB ['888886888', '888888988', '888888880']\n"
                         "555555555 AMB ['559555555', '555655555']\n"
                         "666666666 AMB ['686666666', '666566666']\n"
                         "999999999 AMB ['899999999', '993999999', '999959999']\n"
                         "490067715 AMB ['490867715', '490067115', '490067719']\n"
                         "123456789\n"
                         "000000051\n"
                         "490867715\n")

    def test_big_account(self):
        bank_ocr.guess_multi_accounts('./input.txt')


if __name__ == '__main__':
    unittest.main()
