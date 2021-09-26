import datetime
import string
import random
from tkinter import *
import sqlite3
from tkinter import messagebox
import create_verification_email
import send_test_email
import easygui

class blockchain:
    def __init__(self):
        #  Turn sending emails off so program doesn't send spam to emails
        self.actually_send_emails = False  # e.g. verification emails + password change verification emails
        #  Length of keys/addresses, when marked as used
        self.pub_key_len = 16
        self.priv_key_len = 24
        self.address_len = 12
        #  Whether to make 4 keys i.e. when creating a new wallet need 4
        self.make_4_keys = False
        #  Checking when the windows are open so can know when window was opened twice
        self.listb_key_open = False
        self.wallet_win_is_open = False
        self.win_logged_in_is_open = False
        self.win_deposit_cur_is_open = False
        self.win_wallet_info_is_open = False
        self.win_listb_keys_address_is_open = False
        #  Connect to database and creation of cursor
        self.db_connection = sqlite3.connect('GeoCoin')
        self.cursor = self.db_connection.cursor()

        #  Create main window
        self.main_win = Tk()
        self.main_win.title('User Login')
        self.main_win.geometry('320x395')
        #  Default coordinates for tk objects
        def_x = 65
        def_y = 20

        win_title = Label(self.main_win, text='User Login', font=('TkDefaultFont, 20'))
        win_title.place(x=def_x, y=def_y)
        win_user_guidance = Label(self.main_win, text='Please only use EXIT buttons to quit windows')
        win_user_guidance.place(x=def_x-29, y=def_y+35)

        #  Below variables have the suffix- _for_login so program doesn't
        #  get confused with objects in create wallet method
        self.lab_wallet_name_for_login = Label(self.main_win, text='Wallet Name')
        self.lab_wallet_name_for_login.place(x=def_x+49, y=def_y+75)
        self.ent_wallet_name_for_login = Entry(self.main_win, width=26)
        self.ent_wallet_name_for_login.place(x=def_x+14, y=def_y+100)
        #  Generating passnum characters to enter
        self.passnum_chars_to_ent = []
        for number in range(6):
            randint = random.randint(1, 6)
            self.passnum_chars_to_ent.append(randint)
        self.passnum_chars_to_ent = str(self.passnum_chars_to_ent).replace('[', '')
        self.passnum_chars_to_ent = self.passnum_chars_to_ent.replace(']', '')

        self.txt_passnum_chars_to_ent = 'Enter numbers ' + self.passnum_chars_to_ent + ' from passnumber'
        self.lab_passnum_ent_for_login = Label(self.main_win, text=self.txt_passnum_chars_to_ent)
        self.lab_passnum_ent_for_login.place(x=def_x-31, y=def_y+145)
        self.ent_passnum_for_login = Entry(self.main_win, width=10)
        self.ent_passnum_for_login.place(x=def_x+65, y=def_y+170)

        btn_refresh_win = Button(self.main_win, text='Refresh', borderwidth=3,
                                 command=self.main_win_refresh)
        btn_refresh_win.place(x=def_x+180, y=def_y)
        # Button for creating a new wallet window
        btn_create_wallet = Button(self.main_win, command=self.create_new_wallet_interface,
                                   borderwidth=5, text='Create Wallet')
        btn_create_wallet.place(x=def_x-20, y=def_y+215)
        #  Button to log in with
        btn_validate_user = Button(self.main_win, command=self.log_in,
                                   borderwidth=5, text='Login')
        btn_validate_user.place(x=def_x+162, y=def_y+215)
        #  Button to change the passnum
        btn_forgot_passnum = Button(self.main_win, text='Forgot Passnum [send email]',
                                     borderwidth=3, command=self.forgot_passnum)
        btn_forgot_passnum.place(x=def_x+9, y=def_y+270)

        btn_exit_win = Button(self.main_win, command=self.main_win_quit,
                              borderwidth=4, text='EXIT')
        btn_exit_win.place(x=def_x+78, y=def_y+325)
        self.main_win.mainloop()

    def create_new_wallet_interface(self):
        if self.wallet_win_is_open:  # If this window is already open = Error
            messagebox.showerror('User Error', 'Window already open')
        else:
            win_title = 'Create Wallet'
            def_x = 130
            def_y = 20

            self.wallet_win = Toplevel()
            self.wallet_win.geometry('333x280')
            self.wallet_win.title(win_title)
            self.wallet_win_is_open = True

            lbl_wallet_win_title = Label(self.wallet_win, text=win_title, font=('TkDefaultFont, 18'))
            lbl_wallet_win_title.place(x=def_x-40, y=def_y)

            lbl_wallet_name = Label(self.wallet_win, text='Wallet Name')
            lbl_wallet_name.place(x=def_x-100, y=def_y+60)
            self.ent_wallet_name = Entry(self.wallet_win)
            self.ent_wallet_name.place(x=def_x+40, y=def_y+60)

            lbl_passnumber = Label(self.wallet_win, text='Passnumber \n [min-max length: 6-14]')
            lbl_passnumber.place(x=def_x-100, y=def_y+110)
            self.ent_passnumber = Entry(self.wallet_win)
            self.ent_passnumber.place(x=def_x+40, y=def_y+110)

            lbl_email_ad = Label(self.wallet_win, text='Email Address')
            lbl_email_ad.place(x=def_x-100, y=def_y+160)
            self.ent_email_ad = Entry(self.wallet_win)
            self.ent_email_ad.place(x=def_x+40, y=def_y+160)

            btn_create_wallet = Button(self.wallet_win, text='Create',
                                       command=self.create_new_wallet, borderwidth=4)
            btn_create_wallet.place(x=def_x-48, y=def_y+210)

            btn_exit_win = Button(self.wallet_win, text='EXIT', borderwidth=4,
                                  command=self.create_new_wallet_interface_quit)
            btn_exit_win.place(x=def_x+87, y=def_y+210)

            mainloop()

    def create_new_wallet(self):
        if self.ent_wallet_name.get() == '' or self.ent_passnumber.get() == '' or\
self.ent_email_ad.get() == '':  #  If haven't entered into the requisite fields
            messagebox.showerror('User Error', 'Enter into every field')
        elif self.check_passnum_valid(self.ent_passnumber.get()) == False:  # If passnum invalid
            return  #  Error msg already shown in method
        elif self.check_create_wallet_is_unique() is False:  # If input is not unique
            messagebox.showerror('Unacceptable Input', 'Wallet name already taken')
            self.ent_wallet_name.delete(0, END)
        elif send_test_email.__init__(self.ent_email_ad.get()) == False and\
self.actually_send_emails:  # If isn't legit email and am sending real emails
            messagebox.showerror('Unacceptable Input', 'Email address is not valid')
        else:  # If all 3 inputs are acceptable do the below
            try:
                self.find_next_wal_id()  # For input of the wallet details, find next id
                self.make_4_keys = True
                self.create_keys()  # Make keys and return them for new wallet

                self.gcoin_amount = 0
                self.no_of_transactions = 0

                public_keys = str(self.pub_key_list)
                private_keys = str(self.priv_key_list)
                addresses = str(self.address_list)
                #  To help turn lists into strings of the lists of values
                public_keys = public_keys.replace('[', '')
                public_keys = public_keys.replace(']', '')
                private_keys = private_keys.replace('[', '')
                private_keys = private_keys.replace(']', '')
                addresses = addresses.replace('[', '')
                addresses = addresses.replace(']', '')

                self.get_todate()  # To add to new wallet details

                #  Removal of blank spaces
                self.ent_wallet_name = self.ent_wallet_name.get().strip()
                self.ent_passnumber = self.ent_passnumber.get().strip()
                self.ent_email_ad = self.ent_email_ad.get().strip()

                list_wallet_inputs = [self.next_wal_id, self.ent_wallet_name,
                                      self.gcoin_amount, self.no_of_transactions,
                                      public_keys, private_keys, addresses,
                                      self.ent_passnumber, self.todate,
                                      self.ent_email_ad]
                #  Inputting the new wallet created
                self.cursor.execute('INSERT INTO walletss_info VALUES (?,?,?,?,?,?,?,?,?,?)',
                                    list_wallet_inputs)
                self.db_connection.commit()
                self.wallet_win.destroy()
                self.wallet_win_is_open = False
                #  (try:) if all works, do the below line
                messagebox.showinfo('Success', 'Wallet created')
            except BaseException:
                messagebox.showerror('Operation Error', 'Wallet creation failed')

    def find_next_wal_id(self):
        wallet_ids = self.cursor.execute('SELECT wallet_id from walletss_info')
        self.next_wal_id = None
        #  Removal of commas and brackets from
        for id in wallet_ids:  # Below 4 lines- preparing the last id value
            id = str(id)
            id = id.replace('(', '')
            id = id.replace(')', '')
            id = id.replace(',', '')
            self.next_wal_id = int(id) + 1
        if self.next_wal_id == None:  # If there are no other wallets made
            self.next_wal_id = 1
        return self.next_wal_id

    def create_keys(self):
        # Creation of private key and the subsequent public key and address for
        # each private key.
        all_letters = string.ascii_letters  # All letters of the alphabet
        if self.make_4_keys == True:
            self.priv_key_list = []
            self.pub_key_list = []
            self.address_list = []
            for each_key in range(4):
                #  Private key
                private_key = str()
                for letter in range(self.priv_key_len):
                    rand_pos = random.randrange(len(all_letters))
                    private_key = private_key + all_letters[rand_pos]
                self.priv_key_list.append(private_key)

                #  Public key
                public_key = str()
                public_key = public_key + private_key[0:3]  # First 3 chars, first 3 of private key
                pub_key_rand_len = self.pub_key_len - 3
                for letter in range(pub_key_rand_len):
                    rand_pos = random.randrange(len(private_key))
                    public_key = public_key + private_key[rand_pos]
                self.pub_key_list.append(public_key)

                #  Address
                address = str()
                for letter in range(self.address_len):
                    current_address_char = random.randint(2, 9)
                    address = address + str(current_address_char)
                self.address_list.append(address)

                self.make_4_keys = False
            return self.priv_key_list, self.pub_key_list, self.address_list

        else:
            #  Private key
            self.private_key = str()
            for letter in range(self.priv_key_len):
                rand_pos = random.randrange(len(all_letters))
                self.private_key = self.private_key + all_letters[rand_pos]

            #  Public key
            self.public_key = str()
            self.public_key = self.public_key + self.private_key[0:3]  # First 3 chars, first 3 of private key
            pub_key_rand_len = self.pub_key_len - 3
            for letter in range(pub_key_rand_len):
                rand_pos = random.randrange(len(self.private_key))
                self.public_key = self.public_key + self.private_key[rand_pos]

            #  Address
            self.address = str()
            for letter in range(self.address_len):
                current_address_char = random.randint(2, 9)
                self.address = self.address + str(current_address_char)

            return self.private_key, self.public_key, self.address

    def check_create_wallet_is_unique(self):
        #  Ensure wallet name hasn't been used before
        all_wallet_names = self.cursor.execute('SELECT wallet_name FROM walletss_info')
        wal_name_for_creation = self.ent_wallet_name.get()
        for wallet_name in all_wallet_names:  # Prep of wallet_name
            wallet_name = str(wallet_name).replace('(', '')
            wallet_name = wallet_name.replace(')', '')
            wallet_name = wallet_name.replace(',', '')
            wallet_name = wallet_name.replace("'", '')
            wallet_name = wallet_name.replace("'", '')
            if wallet_name == wal_name_for_creation:  # If is not unique
                return False


    def log_in(self):
        if self.wallet_win_is_open:  # If create wallet win is already open (this
            # method doesn't work)
            messagebox.showerror('User Error', 'Please close Create Wallet first')
        else:
            login_success = False
            num_of_nums_entered_correctly = 0
            #  Removal of blank spaces, improve user experience, and make local
            #  vars
            wallet_name_entered = self.ent_wallet_name_for_login.get().strip()
            passnum_entered = self.ent_passnum_for_login.get().strip()
            if wallet_name_entered == '' or passnum_entered == '':  # If have
                # entered anything into one or both of the details
                messagebox.showerror('User Error', 'Enter wallet name and passnum')
            elif passnum_entered.isnumeric()  == False:
                messagebox.showerror('User Error', 'Passnum must be numeric')
            elif len(passnum_entered) != 6:  # If digits entered are not correct
                # length
                messagebox.showerror('User Error', 'Enter 6 numbers')
            else:  # If wal name and passnum are valid
                wal_name_to_look_for = '"' + wallet_name_entered + '"'
                qry = """SELECT * FROM walletss_info WHERE wallet_name={}"""
                qry = qry.format(wal_name_to_look_for)
                wallet_entered_info = self.cursor.execute(qry)
                is_valid_wal_name = False
                for all_info in wallet_entered_info:
                    # If can iterate means is valid, if can't find anything won't
                    is_valid_wal_name = True  # be able to iterate
                    self.logged_in_wallet_id = all_info[0]
                    self.logged_in_wallet_name = wallet_name_entered
                    self.logged_in_GCoin_amount = all_info[2]
                    self.logged_in_no_of_transactions = all_info[3]
                    self.logged_in_public_keys = all_info[4]
                    self.logged_in_priv_keys = all_info[5]
                    self.logged_in_addresses = all_info[6]
                    self.logged_in_passnumber = all_info[7]
                    self.logged_in_date_of_creation = all_info[8]

                if not is_valid_wal_name:
                    messagebox.showerror('User Error', 'Not a valid wallet name')
                else:  # If is a valid wallet name
                    #  Position of chars to ent
                    list_passnum_chars_to_ent = self.passnum_chars_to_ent.split(',')
                    #  Passnum chars entd
                    list_passnum_entered = list(passnum_entered)
                    #  Wallet passnum chars
                    #  wallet_passnum_chars = self.logged_in_passnumber

                    #  The below works out whether the passnum entered is correct
                    list_wallet_passnum = list(str(self.logged_in_passnumber))
                    ind_pos = 0
                    for passnum_entd in list_passnum_entered:
                        pos_of_char_for_entry = int(list_passnum_chars_to_ent[ind_pos])-1
                        passnum_char_to_ent = list_wallet_passnum[pos_of_char_for_entry]
                        if passnum_entd == passnum_char_to_ent:
                            pass
                        else:
                            messagebox.showerror('User Error', 'Passnum entered incorrectly')
                            return
                        ind_pos += 1
                    self.logged_in_interface()  # Will go unless passnum incorrect

    def fetch_all_wallet_info(self):
        all_wallet_info = self.cursor.execute('SELECT * FROM walletss_info')
        self.wallet_info_list = []
        for wallet_info in all_wallet_info:
            self.wallet_info_list.append(wallet_info)
        return self.wallet_info_list

    def logged_in_interface(self):
        if self.win_logged_in_is_open:
            messagebox.showerror('User Error', 'Window already open')
        else:
            win_title = 'GCoin'
            self.def_x = 60
            self.def_y = 20

            self.win_logged_in = Toplevel()
            self.win_logged_in.geometry('360x280')
            self.win_logged_in.title(win_title)
            self.win_logged_in_is_open = True

            lbl_win_title = Label(self.win_logged_in, text=win_title, font=('TkDefaultFont, 14'))
            lbl_win_title.place(x=self.def_x, y=self.def_y)

            lbl_GCoin_amount = Label(self.win_logged_in, text='Amount')
            lbl_GCoin_amount.place(x=self.def_x-20, y=self.def_y+45)
            lbl_currency_sign = Label(self.win_logged_in, text='G')
            lbl_currency_sign.place(x=self.def_x+77, y=self.def_y+45)
            self.ent_GCoin_amount = Entry(self.win_logged_in, width=15)
            self.ent_GCoin_amount.place(x=self.def_x+90, y=self.def_y+45)

            lbl_sendee_wallet_name = Label(self.win_logged_in, text='Sendee Name')
            lbl_sendee_wallet_name.place(x=self.def_x-20, y=self.def_y+95)
            self.ent_sendee_wallet_name = Entry(self.win_logged_in)
            self.ent_sendee_wallet_name.place(x=self.def_x+90, y=self.def_y+95)

            btn_delete_wallet = Button(self.win_logged_in, text='Delete Wallet',
                                       command=self.delete_wallet,
                                       borderwidth=5)
            btn_delete_wallet.place(x=self.def_x+200, y=self.def_y-10)

            btn_deposit_currency = Button(self.win_logged_in, command=self.deposit_currency_interface,
                                          borderwidth=4, text='Withdraw or Deposit')
            btn_deposit_currency.place(x=self.def_x-22, y=self.def_y+145)

            btn_view_wallet = Button(self.win_logged_in, text='View Wallet',
                                     command=self.view_wallet_interface, borderwidth=4)
            btn_view_wallet.place(x=self.def_x+187, y=self.def_y+145)

            btn_send_currency = Button(self.win_logged_in, text='Send',
                                       command=self.send_currency, borderwidth=6)
            btn_send_currency.place(x=self.def_x+95, y=self.def_y+200)

            btn_exit_win = Button(self.win_logged_in, text='EXIT', borderwidth=4,
                                  command=self.logged_in_win_quit)
            btn_exit_win.place(x=self.def_x+230, y=self.def_y+200)

    def delete_wallet(self):
        confirm_delete_box = easygui.ynbox('''This is a permanent process 
        Do you still wish to proceed?''', 'Confirm')
        if confirm_delete_box == False:  # If press 'No' in ynbox above
            return
        else:  # If press 'Yes' in ynbox above
            try:
                wal_name = "'" + self.logged_in_wallet_name + "'"  # Need to add
                # this for inputting into table otherwise doesn't know is string
                qry = '''DELETE FROM walletss_info WHERE wallet_name={}'''\
                    .format(wal_name)
                self.cursor.execute(qry)
                self.db_connection.commit()
                self.ent_wallet_name_for_login.delete(0, END)
                self.ent_passnum_for_login.delete(0, END)
                self.win_logged_in.destroy()
                self.win_logged_in_is_open = False
                messagebox.showinfo('Success', 'Successfully deleted')
            except BaseException:
                messagebox.showerror('Operation Error', 'Wallet deletion failed')


    def deposit_currency_interface(self):
        if self.win_deposit_cur_is_open:
            messagebox.showerror('User Error', 'Window already open')
        else:
            win_title = 'Deposit or Withdraw'
            def_x = 40
            def_y = 15

            self.win_deposit_cur = Toplevel()
            self.win_deposit_cur.title(win_title)
            self.win_deposit_cur.geometry('320x230')
            self.win_deposit_cur_is_open = True

            lbl_win_title = Label(self.win_deposit_cur, text=win_title, font=('TkDefaultFont, 20'))
            lbl_win_title.place(x=def_x-7, y=def_y)

            list_dep_or_withd = ['Deposit', 'Withdraw']
            self.choice_dep_or_withd = StringVar()
            self.choice_dep_or_withd.set('Type')
            opt_deposit_or_withdraw = OptionMenu(self.win_deposit_cur, self.choice_dep_or_withd,
                                                 *list_dep_or_withd)
            opt_deposit_or_withdraw.place(x=def_x-10, y=def_y+60)

            self.lbl_dep_or_withd_amount = Label(self.win_deposit_cur, text='Amount')
            self.lbl_dep_or_withd_amount.place(x=def_x-10, y=def_y+110)
            self.ent_dep_or_with_amount = Entry(self.win_deposit_cur)
            self.ent_dep_or_with_amount.place(x=def_x+110, y=def_y+110)

            self.btn_move_money = Button(self.win_deposit_cur, text='Execute',
                                         command=self.deposit_currency, borderwidth=6)
            self.btn_move_money.place(x=def_x+90, y=def_y+160)

            btn_win_quit = Button(self.win_deposit_cur, text='EXIT', borderwidth=4,
                                  command=self.win_deposit_cur_quit)
            btn_win_quit.place(x=def_x+222, y=def_y+160)

    def deposit_currency(self):
        if self.choice_dep_or_withd.get() == 'Type':  # Make sure have chosen
            messagebox.showerror('User Error', 'Please choose to deposit or withdraw')
            return  # So rest of method doesn't run
        elif self.ent_dep_or_with_amount.get() == '':  # Make sure have entered an amount
            messagebox.showerror('User Error', 'Must enter an amount')
            return  # So rest of method doesn't run
        else:  # Collect the amount for dep or withd
            dep_or_withd_amount = float(self.ent_dep_or_with_amount.get())

        if dep_or_withd_amount < 0 and self.choice_dep_or_withd.get() == 'Deposit':
            messagebox.showerror('User Error', 'Cannot deposit that amount')
        elif dep_or_withd_amount < 0 and self.choice_dep_or_withd.get() == 'Withdraw':
            messagebox.showerror('User Error', 'Cannot withdraw that amount')
        else:  # If amount is greater than 0
            self.get_todate()
            wal_name = '"' + self.logged_in_wallet_name + '"'  # Needs to be in
            #  speech marks for this SQlite3 as doesn't know is str otherwise
            qry = '''SELECT GCoin_amount FROM walletss_info WHERE wallet_name={}'''\
                .format(wal_name)
            wallet_amount = self.db_connection.execute(qry)
            for wal_amount in wallet_amount:
                wallet_amount = str(wal_amount).replace('(', '')
                wallet_amount = wallet_amount.replace(')', '')
                wallet_amount = wallet_amount.replace(',', '')
                orig_wallet_amount = float(wallet_amount)

            deposits_id = self.db_connection.execute('SELECT deposit_id FROM deposits_info')
            for id in deposits_id:
                id = str(id).replace('(', '')
                id = id.replace(')', '')
                id = id.replace(',', '')
                next_deposit_id = int(id) + 1

            info_for_deposit = [next_deposit_id, self.choice_dep_or_withd.get(),
                                dep_or_withd_amount,
                                self.logged_in_wallet_id,
                                self.logged_in_wallet_name, self.todate]
            self.cursor.execute('INSERT INTO deposits_info VALUES(?,?,?,?,?,?)', info_for_deposit)

            #  Find new amounts for wallets, depending on if is deposit or withdrawal
            if self.choice_dep_or_withd.get() == 'Deposit':
                new_wallet_amount = orig_wallet_amount + dep_or_withd_amount
            else:  # If is a withdrawal
                new_wallet_amount = orig_wallet_amount - dep_or_withd_amount
            if new_wallet_amount < 0:
                messagebox.showerror('User Error', 'Insufficient funds')
                return

            qry = 'UPDATE walletss_info SET GCoin_amount={} WHERE wallet_id={}'\
                .format(new_wallet_amount, self.logged_in_wallet_id)
            change_wallet_amount = self.cursor.execute(qry)
            self.db_connection.commit()

            #  Send the appropriate success message
            if self.choice_dep_or_withd.get() == 'Deposit':
                messagebox.showinfo('Success', 'Deposit Successful')
                self.win_deposit_cur_quit()
                #  So is updated and sending new money can be done without error
                self.update_logged_in_info(self.logged_in_wallet_name)
            else:  # If is a withdrawal
                messagebox.showinfo('Success', 'Withdraw Successful')
                self.win_deposit_cur_quit()
                #  So is updated and sending new money can be done without error
                self.update_logged_in_info(self.logged_in_wallet_name)

    def update_logged_in_info(self, wallet_name):
        wal_name_to_look_for = '"' + wallet_name + '"'
        qry = """SELECT * FROM walletss_info WHERE wallet_name={}"""
        qry = qry.format(wal_name_to_look_for)
        wallet_entered_info = self.cursor.execute(qry)
        is_valid_wal_name = False
        for all_info in wallet_entered_info:
            # If can iterate means is valid, if can't find anything won't
            is_valid_wal_name = True  # be able to iterate
            self.logged_in_wallet_id = all_info[0]
            self.logged_in_wallet_name = wallet_name
            self.logged_in_GCoin_amount = all_info[2]
            self.logged_in_no_of_transactions = all_info[3]
            self.logged_in_public_keys = all_info[4]
            self.logged_in_priv_keys = all_info[5]
            self.logged_in_addresses = all_info[6]
            self.logged_in_passnumber = all_info[7]
            self.logged_in_date_of_creation = all_info[8]


    def view_wallet_interface(self):
        if self.win_wallet_info_is_open:
            messagebox.showerror('User Error', 'Window already open')
        else:
            win_title = 'Your Info'
            def_x = 70
            def_y = 20

            self.win_wallet_info = Toplevel()
            self.win_wallet_info.geometry('240x410')
            self.win_wallet_info.title(win_title)
            self.win_wallet_info_is_open = True

            lbl_win_title = Label(self.win_wallet_info, text=win_title, font=('TkDefaultFont, 20'))
            lbl_win_title.place(x=def_x-5, y=def_y)

            txt_wallet_id = 'Wallet ID- ' + str(self.logged_in_wallet_id)
            lbl_wallet_id = Label(self.win_wallet_info, text=txt_wallet_id)
            lbl_wallet_id.place(x=def_x-30, y=def_y+60)

            txt_wallet_name = 'Wallet Name- ' + str(self.logged_in_wallet_name)
            lbl_wallet_name = Label(self.win_wallet_info, text=txt_wallet_name)
            lbl_wallet_name.place(x=def_x-30, y=def_y+100)

            txt_GCoin_amount = 'GCoin Amount- G' + str(self.logged_in_GCoin_amount)
            lbl_GCoin_amount = Label(self.win_wallet_info, text=txt_GCoin_amount)
            lbl_GCoin_amount.place(x=def_x-30, y=def_y+140)

            txt_no_of_transactions = 'No of Transactions- ' + str(self.logged_in_no_of_transactions)
            lbl_no_of_transactions = Label(self.win_wallet_info, text=txt_no_of_transactions)
            lbl_no_of_transactions.place(x=def_x-30, y=def_y+180)

            self.btn_view_keys_and_address = Button(self.win_wallet_info, command=self.view_keys_and_address_interface,
                                                    text='View Keys and Addresses',
                                                    borderwidth=3)
            self.btn_view_keys_and_address.place(x=def_x-30, y=def_y+216)

            txt_passnumber = 'Passnumber- ' + str(self.logged_in_passnumber)
            lbl_passnumber = Label(self.win_wallet_info, text=txt_passnumber)
            lbl_passnumber.place(x=def_x-30, y=def_y+260)

            txt_date_of_creation = 'Date of creation- ' + str(self.logged_in_date_of_creation)
            lbl_date_of_creation = Label(self.win_wallet_info, text=txt_date_of_creation)
            lbl_date_of_creation.place(x=def_x-30, y=def_y+300)

            btn_exit_win = Button(self.win_wallet_info, text='EXIT', borderwidth=4,
                                  command=self.win_wallet_info_quit)
            btn_exit_win.place(x=def_x+38, y=def_y+340)

    def view_keys_and_address_interface(self):
        if self.win_listb_keys_address_is_open:
            messagebox.showerror('User Error', 'Window already open')
        else:
            self.win_listb_keys_address = Toplevel()
            self.win_listb_keys_address.title('Your Keys and Addresses')
            self.win_listb_keys_address_is_open = True
            self.listb_key_open = True  # So self.win_listb_keys_address is known to be open

            lbl_public_keys = Label(self.win_listb_keys_address, text='Public Keys')
            lbl_priv_keys = Label(self.win_listb_keys_address, text='Private Keys')
            lbl_addresses = Label(self.win_listb_keys_address, text='Addresses')
            listb_public_keys = Listbox(self.win_listb_keys_address, width=26)
            listb_priv_keys = Listbox(self.win_listb_keys_address, width=37)
            listb_addresses = Listbox(self.win_listb_keys_address, width=17)
            win_quit = Button(self.win_listb_keys_address, borderwidth=4, text='EXIT',
                              command=self.win_listb_keys_address_quit)
            for key in self.logged_in_public_keys.split():
                listb_public_keys.insert(END, key)
            for key in self.logged_in_priv_keys.split():
                listb_priv_keys.insert(END, key)
            for key in self.logged_in_addresses.split():
                listb_addresses.insert(END, key)
            lbl_public_keys.pack()
            listb_public_keys.pack()
            lbl_priv_keys.pack()
            listb_priv_keys.pack()
            lbl_addresses.pack()
            listb_addresses.pack()
            win_quit.pack()

    def send_currency(self):
        # checking if less than or equal to 0
        if self.ent_GCoin_amount.get() == '':  # If entered nothing
            messagebox.showerror('User Error', 'Enter GCoin amount')
        elif self.ent_sendee_wallet_name.get() == '':  # If entered nothing
            messagebox.showerror('User Error', 'Choose a sendee first')
        else:
            GCoin_amount_as_int = float(self.ent_GCoin_amount.get())  # For use
            if GCoin_amount_as_int <= 0:  # If amount is nothing or negative
                self.ent_GCoin_amount.delete(0, 'end')
                messagebox.showerror('User Error', 'Cannot send that amount')
            else:  # If two inputs are valid
                try:  # If all can be done without error, then do that
                    #  2 Below needs extra "" so is acceptable in sqlite query
                    #  otherwise sqlite thinks is not string
                    self.sendee_wal_name = '"' + self.ent_sendee_wallet_name.get() + '"'
                    self.sender_wal_name = "'" + self.logged_in_wallet_name + "'"
                    #  Validate sendee is valid
                    qry = '''SELECT wallet_name FROM walletss_info WHERE wallet_name
                    ={}'''.format(self.sendee_wal_name)
                    self.sendee_wal_name = self.cursor.execute(qry)
                    for tuple in self.sendee_wal_name:
                        self.sendee_wal_name = str(tuple).replace('(', '')
                        self.sendee_wal_name = self.sendee_wal_name.replace(')', '')
                        self.sendee_wal_name = self.sendee_wal_name.replace(',', '')
                    self.sendee_wal_name_entd = "'" + self.ent_sendee_wallet_name.get() + "'"

                    #  The below- check that aren't trying to send to themselves
                    if self.sender_wal_name == self.sendee_wal_name_entd:
                        messagebox.showerror('User Error', "Can't send to yourself")
                        return
                    #  The below- check that wallet entered is actually in wallets table (legit)
                    elif self.sendee_wal_name != self.sendee_wal_name_entd:
                        messagebox.showerror('User Error', 'Not valid sendee name')
                        return
                    #  Else: do the below
                    #  Collecting info on the sender
                    self.sender_wal_name = self.sender_wal_name
                    qry = '''SELECT GCoin_amount, no_of_transactions, public_keys, 
                    private_keys, addresses FROM walletss_info WHERE wallet_name={}'''\
                        .format(self.sender_wal_name)
                    wallet_for_update = self.cursor.execute(qry)
                    #  below .splits turn strings of lists into lists
                    for info in wallet_for_update:
                        old_GCoin_amount = info[0]
                        old_no_of_transactions = info[1]
                        old_public_keys = info[2].split(', ')
                        old_private_keys = info[3].split(', ')
                        old_addresses = info[4].split(', ')

                    new_sender_GCoin_amount = old_GCoin_amount - float(self.ent_GCoin_amount.get())
                    if new_sender_GCoin_amount < 0:  # Ensure funds are sufficient for req
                        self.ent_GCoin_amount.delete(0, 'end')
                        messagebox.showerror('User Error', 'Insufficient funds')
                        return
                    new_sender_no_of_transactions = old_no_of_transactions + 1
                    #  Manipulation of infos
                    self.remove_extra_speech_marks_from_keys_extracted(old_public_keys,
                                                                old_private_keys, old_addresses)
                    old_public_keys = self.public_keys_single_speech_marks
                    old_private_keys = self.private_keys_single_speech_marks
                    old_addresses = self.addresses_single_speech_marks

                    #  Below are 3 examples of updating of last keys to show been used
                    #  until line 693
                    ind_pos = 0
                    last_ind_pos = len(old_public_keys) - 1
                    for key in old_public_keys:
                        if len(key) == self.pub_key_len:  # If is unused key
                            updated_key = '<' + key + '>'
                            old_public_keys.pop(ind_pos)
                            old_public_keys.insert(ind_pos, updated_key)
                            break
                        elif ind_pos == last_ind_pos:  # If are only used keys
                            self.create_keys()
                            updated_key = '<' + self.public_key + '>'
                            old_public_keys.append(updated_key)
                        ind_pos += 1
                    sender_updated_public_keys = old_public_keys

                    ind_pos = 0
                    last_ind_pos = len(old_private_keys) - 1
                    for key in old_private_keys:
                        if len(key) == self.priv_key_len:  # If is unused key
                            updated_key = '<' + key + '>'
                            old_private_keys.pop(ind_pos)
                            old_private_keys.insert(ind_pos, updated_key)
                            break
                        elif ind_pos == last_ind_pos:  # If are only used keys
                            self.create_keys()
                            updated_key = '<' + self.private_key + '>'
                            old_private_keys.append(updated_key)
                        ind_pos += 1
                    sender_updated_private_keys = old_private_keys

                    ind_pos = 0
                    last_ind_pos = len(old_addresses) - 1
                    for key in old_addresses:  # If is unused key
                        if len(key) == self.address_len:
                            updated_key = '11' + key
                            old_sender_address_for_input = key
                            old_addresses.pop(ind_pos)
                            old_addresses.insert(ind_pos, updated_key)
                            break
                        elif ind_pos == last_ind_pos:  # If are only used keys
                            self.create_keys()
                            old_sender_address_for_input = self.address
                            updated_key = '11' + self.address
                            old_addresses.append(updated_key)
                        ind_pos += 1
                    sender_updated_addresses = old_addresses

                    self.change_lists_into_string(sender_updated_public_keys,
                                                  sender_updated_private_keys,
                                                  sender_updated_addresses)

                    #  Adding speech marks onto ends of entire strings so is SQLite3
                    #  acceptable
                    self.public_keys_as_string = '"' + self.public_keys_as_string + '"'
                    self.private_keys_as_string = '"' + self.private_keys_as_string + '"'
                    self.addresses_as_string = '"' + self.addresses_as_string + '"'

                    sender_updated_public_keys = self.public_keys_as_string
                    sender_updated_private_keys = self.private_keys_as_string
                    sender_updated_addresses = self.addresses_as_string

                    #  Collecting info on sendee
                    self.sendee_wal_name = self.sendee_wal_name
                    qry = '''SELECT GCoin_amount, no_of_transactions, public_keys, 
                    private_keys, addresses FROM walletss_info
                        WHERE wallet_name={}'''.format(self.sendee_wal_name)
                    old_sendee_info = self.cursor.execute(qry)
                    #  .split() turns strings of lists into strings
                    for info in old_sendee_info:
                        old_GCoin_amount = info[0]
                        old_no_of_transactions = info[1]
                        old_public_keys = info[2].split(', ')
                        old_private_keys = info[3].split(', ')
                        old_addresses = info[4].split(', ')

                    new_sendee_GCoin_amount = old_GCoin_amount + float(self.ent_GCoin_amount.get())
                    new_sendee_no_of_transactions = old_no_of_transactions + 1

                    self.remove_extra_speech_marks_from_keys_extracted(old_public_keys,
                                                                       old_private_keys, old_addresses)
                    old_public_keys = self.public_keys_single_speech_marks
                    old_private_keys = self.private_keys_single_speech_marks
                    old_addresses = self.addresses_single_speech_marks

                    #  Below are 3 examples of updating of last keys to show been used
                    #  until line 693
                    ind_pos = 0
                    last_ind_pos = len(old_public_keys) - 1
                    for key in old_public_keys:
                        if len(key) == self.pub_key_len:  # If is unused key
                            updated_key = '<' + key + '>'
                            old_public_keys.pop(ind_pos)
                            old_public_keys.insert(ind_pos, updated_key)
                            break
                        elif ind_pos == last_ind_pos:  # If are only used keys
                            self.create_keys()
                            updated_key = '<' + self.public_key + '>'
                            old_public_keys.append(updated_key)
                        ind_pos += 1
                    sendee_updated_public_keys = old_public_keys

                    ind_pos = 0
                    last_ind_pos = len(old_private_keys)-1
                    for key in old_private_keys:
                        if len(key) == self.priv_key_len:  # If is unused key
                            updated_key = '<' + key + '>'
                            old_private_keys.pop(ind_pos)
                            old_private_keys.insert(ind_pos, updated_key)
                            break
                        elif ind_pos == last_ind_pos:  # If are only used keys
                            self.create_keys()
                            updated_key = '<' + self.private_key + '>'
                            old_private_keys.append(updated_key)
                        ind_pos += 1
                    sendee_updated_private_keys = old_private_keys

                    ind_pos = 0
                    last_ind_pos = len(old_addresses) - 1
                    for key in old_addresses:
                        if len(key) == self.address_len:  # If is unused key
                            updated_key = '11' + key
                            old_sendee_address_for_input = key
                            old_addresses.pop(ind_pos)
                            old_addresses.insert(ind_pos, updated_key)
                            break
                        elif ind_pos == last_ind_pos:  # If are only used keys
                            self.create_keys()
                            old_sendee_address_for_input = self.address
                            updated_key = '11' + self.address
                            old_addresses.append(updated_key)
                        ind_pos += 1
                    sendee_updated_addresses = old_addresses

                    self.change_lists_into_string(sendee_updated_public_keys,
                                                  sendee_updated_private_keys,
                                                  sendee_updated_addresses)

                    #  Adding speech marks onto ends of entire strings so is SQLite3 acceptable
                    self.public_keys_as_string = '"' + self.public_keys_as_string + '"'
                    self.private_keys_as_string = '"' + self.private_keys_as_string + '"'
                    self.addresses_as_string = '"' + self.addresses_as_string + '"'

                    sendee_updated_public_keys = self.public_keys_as_string
                    sendee_updated_private_keys = self.private_keys_as_string
                    sendee_updated_addresses = self.addresses_as_string

                    #  Collecting transactions table info
                    self.get_todate()  # Today's date
                    self.todate = '"' + self.todate + '"'

                    self.generate_new_trans_id()

                    #  For updating previous trans id, removal of preceding '99'
                    updated_last_trans_id = self.last_transaction_id[2:]

                    #  Changing the currency and the infos, on the sender wallet
                    sender_wallet_info = [new_sender_GCoin_amount, new_sender_no_of_transactions,
                                          sender_updated_public_keys, sender_updated_private_keys,
                                          sender_updated_addresses, self.sender_wal_name]
                    qry = '''UPDATE walletss_info SET GCoin_amount={}, no_of_transactions={},
                    public_keys={}, private_keys={}, addresses={} WHERE wallet_name={}'''
                    qry = qry.format(sender_wallet_info[0], sender_wallet_info[1],
                                     sender_wallet_info[2], sender_wallet_info[3],
                                     sender_wallet_info[4], sender_wallet_info[5])
                    self.cursor.execute(qry)

                    #  Changing the currency and the infos, on the sendee wallet
                    sendee_wallet_info = [new_sendee_GCoin_amount, new_sendee_no_of_transactions,
                                          sendee_updated_public_keys, sendee_updated_private_keys,
                                          sendee_updated_addresses, self.sendee_wal_name]
                    qry = '''UPDATE walletss_info SET GCoin_amount={}, no_of_transactions={},
                    public_keys={}, private_keys={}, addresses={} WHERE wallet_name={}'''
                    qry = qry.format(sendee_wallet_info[0], sendee_wallet_info[1], sendee_wallet_info[2],
                                     sendee_wallet_info[3], sendee_wallet_info[4], sendee_wallet_info[5])
                    self.cursor.execute(qry)

                    #  Update previous transaction's hash/id
                    info_for_update_trans_id = [updated_last_trans_id, self.last_transaction_id]
                    qry = '''UPDATE transactions_info SET transaction_id={} WHERE
                    transaction_id={}'''
                    qry = qry.format(info_for_update_trans_id[0], info_for_update_trans_id[1])
                    self.cursor.execute(qry)

                    #  Updating transactions table with new transaction
                    info_for_send_cur = [self.new_transaction_id, self.logged_in_wallet_name,
                                         old_sender_address_for_input,
                                         self.ent_sendee_wallet_name.get(),
                                         old_sendee_address_for_input,
                                         self.ent_GCoin_amount.get(),
                                         self.todate]
                    qry = '''INSERT INTO transactions_info VALUES({},{},{},{},{},{},{})'''
                    info_for_send_cur[1] = '"' + info_for_send_cur[1] + '"'
                    info_for_send_cur[3] = '"' + info_for_send_cur[3] + '"'
                    qry = qry.format(info_for_send_cur[0], info_for_send_cur[1], info_for_send_cur[2],
                                     info_for_send_cur[3], info_for_send_cur[4], info_for_send_cur[5],
                                     info_for_send_cur[6])
                    self.cursor.execute(qry)
                    self.db_connection.commit()

                    self.ent_GCoin_amount.delete(0, 'end')
                    self.ent_sendee_wallet_name.delete(0, 'end')
                    #  So is updated and sending new money can be done without error
                    self.update_logged_in_info(self.logged_in_wallet_name)
                    messagebox.showinfo('Success', 'Money sent')
                except BaseException:
                    messagebox.showerror('Operation Error', 'Money could not be sent')

    def generate_new_trans_id(self):
        self.all_transaction_ids = self.cursor.execute('SELECT transaction_id FROM transactions_info')
        self.all_transaction_ids_list = []
        for trans_id in self.all_transaction_ids:
            trans_id = str(trans_id).replace('(', '')
            trans_id = trans_id.replace(')', '')
            trans_id = trans_id.replace(',', '')
            self.all_transaction_ids_list.append(trans_id)
            if len(trans_id) == 12:  # If is the last used id
                self.last_transaction_id = trans_id

        self.new_transaction_id = ''
        ind_pos = 0
        for number in self.last_transaction_id:  # 12 digits looped over
            if ind_pos == 0 or ind_pos == 1:  # 2 digits to show is latest block
                # To indicate is the latest id [below]
                self.new_transaction_id = self.new_transaction_id + '9'
            # 4 Digits added to new trans_id based on previous latest id
            elif ind_pos == 2 or ind_pos == 3 or ind_pos == 4 or ind_pos == 5:
                number = int(number)  # So if statement works and conversion
                # to string & addition works
                if number != 9:
                    number = number + 1
                    self.new_transaction_id = self.new_transaction_id + str(number)
                else:  # If number is 9, can't be incremented same way so do below
                    number = str(0)
                    self.new_transaction_id = self.new_transaction_id + number
            else:  # Last 6 digits added are totally random
                randint = random.randint(0, 9)
                self.new_transaction_id = self.new_transaction_id + str(randint)
            ind_pos += 1

        for id in self.all_transaction_ids_list:  # Check its uniqueness
            if self.new_transaction_id == id:
                self.generate_new_trans_id()

        #  Return the last id- so know which one to replace and the new transa
        #  ction_id to replace the last_id to
        return self.new_transaction_id, self.last_transaction_id, \
               self.new_transaction_id

    def forgot_passnum(self):
        #  [below] so can find wallet name in sqlite3
        self.wallet_name_forgot = '"' + self.ent_wallet_name_for_login.get() + '"'
        if self.wallet_name_forgot == '""':  # If nothing entered
            messagebox.showerror('User Error', 'No wallet name chosen')
            return
        else:
            qry = '''SELECT email_address FROM walletss_info WHERE wallet_name={}'''
            qry = qry.format(self.wallet_name_forgot)
            email_address_for_forgot = self.cursor.execute(qry)
            is_valid_wallet_name = False

            for the_address in email_address_for_forgot:
                #  If can iterate then is valid wallet_name so below is True
                is_valid_wallet_name = True
                the_address = str(the_address).replace('(', '')
                the_address = the_address.replace(')', '')
                the_address = the_address.replace(',', '')
                the_address = the_address.replace("'", '')
                the_address = the_address.replace("'", '')
            if not is_valid_wallet_name:  # If wallet name is not valid
                messagebox.showerror('User Error', 'Wallet name not valid')
            else:
                verification_code = ''  # Generate verification code to change it
                for num in range(6):
                    character_for_code = str(random.randint(0, 9))
                    verification_code = verification_code + character_for_code

                was_send_successful_or_shown_successful = True
                if self.actually_send_emails:  # If want to send verif email
                    #  Send email
                    verification_info = create_verification_email.smtp_connection(the_address,
                                        password, verification_code)
                    if verification_info == False:  # If could not send email
                        was_send_successful_or_shown_successful = False
                        messagebox.showerror('Operation Error', 'Could not send email')
                else:  # If want to provide verif code by Python comp not email
                    print('Your verification code (as not going to email in practice program)= '\
                          + verification_code)
                ent_verification_code = easygui.passwordbox('Enter verification code sent',
                                                        'User Verification')
                # If pressed ok on above window or email was sent successfully
                if ent_verification_code != None or\
                        was_send_successful_or_shown_successful:
                    if verification_code == ent_verification_code:  # If ent correctly
                        # Load the interface for entry of new passnum
                        self.ent_new_passnum_for_forgot_passnum()
                    else:
                        messagebox.showerror('User Error', 'Verification code incorrect')
                        ent_verification_code = easygui.passwordbox('Enter verification code sent',
                                                                    'User Verification')
                elif was_send_successful_or_shown_successful == False:  # If failed to send
                    messagebox.showerror('Operation Error', 'Verification email could not send')
                else:  # If pressed cancel or could not send email
                    return

    def ent_new_passnum_for_forgot_passnum(self):
        passbox_field_names = ['Passnum', 'Passnum']
        ent_passnum = easygui.multpasswordbox('Enter and confirm new passnum',
                                              'Passnum Entry', passbox_field_names)
        if ent_passnum == None:  # If pressed cancel
            return
        elif ent_passnum[0] != ent_passnum[1]:  # passnums entd don't match
            messagebox.showerror('User Error', 'Passnums entered do not match')
            self.ent_new_passnum_for_forgot_passnum()
        # If passnum entered is invalid
        elif self.check_passnum_valid(ent_passnum[0]) == False:
            #  Error messages given in method used
            self.ent_new_passnum_for_forgot_passnum()  # Allow to enter again
        else:  # Passnums entd match so below only needs to check one of what
            # passnum was entered (ent_passnum[0])
            if self.check_passnum_valid(ent_passnum[0]):  # (If ==True)
                try:  # Unless there is BaseException do...
                    passnum_entd = str(ent_passnum[0]).replace('[', '')
                    passnum_entd = passnum_entd.replace(']', '')
                    qry = '''UPDATE walletss_info SET passnumber={} WHERE 
                    wallet_name={}'''
                    qry = qry.format(passnum_entd, self.wallet_name_forgot)
                    self.cursor.execute(qry)  # Set new passnum
                    self.db_connection.commit()
                    messagebox.showinfo('Success', 'Passnum changed successfully')
                except BaseException:  # If error then break the above and
                    messagebox.showerror('Operation Error', 'Passnum not updated')
            else:
                pass  # Error msg already in method

    def check_passnum_valid(self, passnum):
        if passnum.isnumeric() == False:
            messagebox.showerror('User Error', 'Passnumber must be numeric')
            return False
        elif len(passnum) > 14:
            messagebox.showerror('User Error', 'Passnumber too long')
            return False
        elif len(passnum) < 6:
            messagebox.showerror('User Error', 'Passnumber too short')
            return False
        else:  # If does not break any of above errors
            return True


    def change_lists_into_string(self, public_keys, private_keys, addresses):
        self.public_keys_as_string = str(public_keys).replace('[', '')
        self.public_keys_as_string = self.public_keys_as_string.replace(']', '')

        self.private_keys_as_string = str(private_keys).replace('[', '')
        self.private_keys_as_string = self.private_keys_as_string.replace(']', '')

        self.addresses_as_string = str(addresses).replace('[', '')
        self.addresses_as_string = self.addresses_as_string.replace(']', '')

        return self.public_keys_as_string, self.private_keys_as_string,\
            self.addresses_as_string

    def remove_extra_speech_marks_from_keys_extracted(self, public_keys, private_keys, addresses):
        #  Removing extra speech marks from each list item
        ind_pos = 0
        for key in public_keys:
            public_keys.pop(ind_pos)
            key = key.replace("'", '')
            updated_key = key.replace("'", '')
            public_keys.insert(ind_pos, updated_key)
            ind_pos += 1
        self.public_keys_single_speech_marks = public_keys

        ind_pos = 0
        for key in private_keys:
            private_keys.pop(ind_pos)
            key = key.replace("'", '')
            updated_key = key.replace("'", '')
            private_keys.insert(ind_pos, updated_key)
            ind_pos += 1
        self.private_keys_single_speech_marks = private_keys

        ind_pos = 0
        for key in addresses:
            addresses.pop(ind_pos)
            key = key.replace("'", '')
            updated_key = key.replace("'", '')
            addresses.insert(ind_pos, updated_key)
            ind_pos += 1
        self.addresses_single_speech_marks = addresses

        return self.public_keys_single_speech_marks,\
               self.private_keys_single_speech_marks,\
                self.addresses_single_speech_marks

    def get_todate(self):
        self.todate = datetime.datetime.today()
        self.todate = self.todate.strftime("%d/%m/%Y")
        return self.todate


    def main_win_refresh(self):
        self.main_win.destroy()
        self.__init__()

    def main_win_quit(self):
        quit()  # Rather than window destroy as i think it is a better way to quit

    def create_new_wallet_interface_quit(self):
        self.wallet_win.destroy()
        self.wallet_win_is_open = False

    def logged_in_win_quit(self):
        self.win_logged_in.destroy()
        self.win_logged_in_is_open = False
        #  If other tk windows open will shut them too
        if self.win_deposit_cur_is_open:
            self.win_deposit_cur.destroy()
            self.win_deposit_cur_is_open = False
        if self.win_wallet_info_is_open:
            self.win_wallet_info.destroy()
            self.win_wallet_info_is_open = False
        if self.win_listb_keys_address_is_open:
            self.win_listb_keys_address.destroy()
            self.win_listb_keys_address_is_open = False

    def win_deposit_cur_quit(self):
        self.win_deposit_cur.destroy()
        self.win_deposit_cur_is_open = False

    def win_wallet_info_quit(self):
        self.win_wallet_info.destroy()
        if self.listb_key_open:  # If it does exist
            self.win_listb_keys_address.destroy()
        self.listb_key_open = False  # So self.win_listb_keys_address is known to not be open
        self.win_wallet_info_is_open = False
        #  In case user quits the above window without closing the below itself
        self.win_listb_keys_address_is_open = False

    def win_listb_keys_address_quit(self):
        self.win_listb_keys_address.destroy()
        self.win_listb_keys_address_is_open = False

        
blockchain()


