import pandas as pd
import numpy as np

path1 = r"C:\Users\Graziela Santana\Desktop\TCC\Solubilidade\Treino_independente.xlsx"
independente = pd.read_excel(path1)
path2 = r"C:\Users\Graziela Santana\Desktop\TCC\Solubilidade\Treino_alvo.xlsx"
alvo = pd.read_excel(path2)

from xgboost import XGBRegressor
xgboost_model = XGBRegressor(reg_lambda=0.000822,alpha=8*10**-8,subsample=0.50,n_estimators=957, max_depth=4, learning_rate=0.061, objective="reg:squarederror", random_state=10,eval_metric='rmse')
xgboost_model.fit(independente, alvo)
import wx

class SimuladorFrame(wx.Frame):
    def __init__(self, parent, title):
        super(SimuladorFrame, self).__init__(parent, title=title, size=(300, 200))

        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(107, 157, 203))
        vbox = wx.BoxSizer(wx.VERTICAL)

        font_bold = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        self.label_temp = wx.StaticText(panel, label='Temperatura em K:', style=wx.ALIGN_CENTER_HORIZONTAL)
        self.label_temp.SetFont(font_bold)
        self.input_temp = wx.TextCtrl(panel, style=wx.ALIGN_CENTER_HORIZONTAL)

        self.label_press = wx.StaticText(panel, label='Pressão em MPa:', style=wx.ALIGN_CENTER_HORIZONTAL)
        self.label_press.SetFont(font_bold)
        self.input_press = wx.TextCtrl(panel, style=wx.ALIGN_CENTER_HORIZONTAL)

        self.label_mol = wx.StaticText(panel, label='Salinidade em mol/kg:', style=wx.ALIGN_CENTER_HORIZONTAL)
        self.label_mol.SetFont(font_bold)
        self.input_mol = wx.TextCtrl(panel, style=wx.ALIGN_CENTER_HORIZONTAL)

        self.button_calcular = wx.Button(panel, label='Calcular')
        self.button_calcular.Bind(wx.EVT_BUTTON, self.calcular_solubilidade)

        self.result_label = wx.StaticText(panel, label='', style=wx.ALIGN_CENTER_HORIZONTAL)
        self.result_label.SetFont(font_bold)

        vbox.Add(self.label_temp, flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=10)
        vbox.Add(self.input_temp, flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=10)
        vbox.Add(self.label_press, flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=10)
        vbox.Add(self.input_press, flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=10)
        vbox.Add(self.label_mol, flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=10)
        vbox.Add(self.input_mol, flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=10)
        vbox.Add(self.button_calcular, flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER, border=10)
        vbox.Add(self.result_label, flag=wx.ALL | wx.ALIGN_CENTER, border=10)

        # Carregar a imagem de fundo
        background_img = wx.Bitmap("background.jpg", wx.BITMAP_TYPE_ANY)
        background_bitmap = wx.StaticBitmap(panel, -1, background_img, style=wx.ALIGN_CENTER)
        vbox.Add(background_bitmap, proportion=1, flag=wx.EXPAND)

        panel.SetSizer(vbox)

    def calcular_solubilidade(self, event):
        try:
            Temp = float(self.input_temp.GetValue())
            Press = float(self.input_press.GetValue())
            Mol = float(self.input_mol.GetValue())
            mp = Mol / Press
            mt = Mol / Temp

            dados = [[Temp,Press,Mol,mp,mt]]
            informacoes = pd.DataFrame(dados,columns = ['Temp','Press','Mol','mp','mt'])
            sol = xgboost_model.predict(informacoes)

            self.result_label.SetLabel('A porcentagem molar do CO2 nessas condições é de {:.2f}%'.format(sol[0]))

        except ValueError:
            self.result_label.SetLabel('Por favor, insira valores válidos.')

app = wx.App(False)
frame = SimuladorFrame(None, 'Simulador de Solubilidade de CO2')
frame.Show()
app.MainLoop()