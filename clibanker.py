#    https://launchpad.net/wxbanker
#    clibanker.py: Copyright 2007, 2008 Mike Rooney <michael@wxbanker.org>
#
#    This file is part of wxBanker.
#
#    wxBanker is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    wxBanker is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with wxBanker.  If not, see <http://www.gnu.org/licenses/>.


def wait():
    raw_input("Press enter to continue...")

def _queryDate():
    date = raw_input("Date (leave blank for today) (MM/DD[/YYYY]): ")
    if len(date.split("/")) == 2:
        # If they didn't include the year, assume the current one.
        date += "/" + str(time.gmtime()[0])
    return date

def _selectAccount(accountNames):
    accountlist = {}
    for i, x in enumerate(sorted(accountNames)):
        accountlist[i] = x
    accountnum = input("Account?\n"+"\n".join( [ str(i+1)+". "+accountlist[i] for i in accountlist] )+"\n? ")
    accountname = accountlist[accountnum-1]
    clearScreen()
    return accountname

def clearScreen():
    os.system(['clear','cls'][os.name == 'nt'])

def main(bankController):
    """
    If we are running the actual file, create a command-line
    interface that the user can use.
    """

    choice = -1
    while choice != 0:
        clearScreen()
        print '1. Create an account'
        print '2. Enter a transaction'
        print '3. Enter a transfer'
        print '4. View Balances'
        print '5. View Transactions'
        print '6. Remove Account'
        print '0. Quit'
        choice = input("? ")

        clearScreen()

        if choice == 1:
            accountName = raw_input("Account name: ")
            bank.createAccount(accountName)
            bank.save()
            wait()

        elif choice == 2:
            accountName = _selectAccount(bank.getAccountNames())
            amount = input("Amount: $")
            desc = raw_input("Description: ")
            date = _queryDate()
            bank.makeTransaction(accountName, amount, desc, date)
            bank.save()
            print 'Transaction successful.'
            wait()

        elif choice == 3:
            print 'From:'
            source = _selectAccount(bank.getAccountNames())
            print 'To:'
            destination = _selectAccount(bank.getAccountNames())
            amount = input('Amount: $')
            desc = raw_input('Description (optional): ')

            confirm = -1
            while confirm == -1 or confirm.lower() not in ['y', 'n']:
                confirm = raw_input('Transfer %s from %s to %s? [y/n]: '%( bank.float2str(amount), source, destination ))

            if confirm == 'y':
                date = _queryDate()
                bank.makeTransfer(source, destination, amount, desc, date)
                bank.save()
                print 'Transfer successfully entered.'
            else:
                print 'Transfer cancelled.'
            wait()

        elif choice == 4:
            total = 0
            for account in sorted(bank.getAccountNames()):
                balance = bank.getBalanceOf(account)
                print "%s %s"%( (account+':').ljust(20), bank.float2str(balance, 10))
                total += balance
            print "%s %s"%( "Total:".ljust(20), bank.float2str(total, 10))

            wait()

        elif choice == 5:
            accountname = _selectAccount(bank.getAccountNames())
            total = 0.0
            for transaction in bank.getTransactionsFrom(accountname):
                uid, amount, desc, date = transaction
                total += amount
                print "%s - %s  %s %s"%( date.strftime('%m/%d/%Y'), desc[:25].ljust(25), bank.float2str(amount, 10), bank.float2str(total, 10) )
            print "Total: %s"%bank.float2str(total)

            wait()

        elif choice == 6:
            accountName = _selectAccount(bank.getAccountNames())
            confirm = -1
            while confirm == -1 or confirm.lower() not in ['y', 'n']:
                confirm = raw_input('Permanently remove account "%s"? [y/n]: '%accountName)
            if confirm == 'y':
                bank.removeAccount(accountName)
                bank.save()
                print 'Account successfully removed'
            else:
                print 'Account removal cancelled'
            wait()
            
            
if __name__ == "__main__":
    print "To run the command-line version of wxBanker, run with the 