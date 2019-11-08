#include "widget.h"
#include "ui_widget.h"
#include <QTcpSocket>
#include "singleton.h"

Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);
}

Widget::~Widget()
{
    delete ui;
}

void Widget::appendMessage(const QString &message)
{
    ui->textBrowser->append(message);
}

void Widget::on_btnForward_pressed()
{
    QString message = "up";
    SingleTon<QTcpSocket>::getInstance()->write(message.toUtf8());
}

void Widget::on_btnForward_released()
{
    QString message = "stop";
    SingleTon<QTcpSocket>::getInstance()->write(message.toUtf8());
}

void Widget::on_btnBack_pressed()
{
    QString message = "down";
    SingleTon<QTcpSocket>::getInstance()->write(message.toUtf8());
}

void Widget::on_btnBack_released()
{
    QString message = "stop";
    SingleTon<QTcpSocket>::getInstance()->write(message.toUtf8());
}

void Widget::on_btnLeft_pressed()
{
    QString message = "left";
    SingleTon<QTcpSocket>::getInstance()->write(message.toUtf8());
}

void Widget::on_btnLeft_released()
{
    QString message = "stop";
    SingleTon<QTcpSocket>::getInstance()->write(message.toUtf8());
}

void Widget::on_btnRight_pressed()
{
    QString message = "right";
    SingleTon<QTcpSocket>::getInstance()->write(message.toUtf8());
}

void Widget::on_btnRight_released()
{
    QString message = "stop";
    SingleTon<QTcpSocket>::getInstance()->write(message.toUtf8());
}

void Widget::on_btnAccelerate_clicked()
{
    QString message = "speedup";
    SingleTon<QTcpSocket>::getInstance()->write(message.toUtf8());
}

void Widget::on_btnSlow_clicked()
{
    QString message = "slowdown";
    SingleTon<QTcpSocket>::getInstance()->write(message.toUtf8());
}

void Widget::on_cbAuto_clicked()
{
    if(ui->cbAuto->checkState() == false){
        QString message = "normal";
        SingleTon<QTcpSocket>::getInstance()->write(message.toUtf8());
        ui->btnBack->setEnabled(true);
        ui->btnForward->setEnabled(true);
        ui->btnLeft->setEnabled(true);
        ui->btnRight->setEnabled(true);
        ui->cbUltraSound->setEnabled(true);
        ui->cbSoundControl->setEnabled(true);
    }else {
        QString message = "auto";
        SingleTon<QTcpSocket>::getInstance()->write(message.toUtf8());
        ui->btnBack->setEnabled(false);
        ui->btnForward->setEnabled(false);
        ui->btnLeft->setEnabled(false);
        ui->btnRight->setEnabled(false);
        ui->cbUltraSound->setEnabled(false);
        ui->cbSoundControl->setEnabled(false);
    }
}

void Widget::on_cbUltraSound_clicked()
{
    if(ui->cbUltraSound->checkState() == false){
        QString message = "normal";
        SingleTon<QTcpSocket>::getInstance()->write(message.toUtf8());
        ui->btnBack->setEnabled(true);
        ui->btnForward->setEnabled(true);
        ui->btnLeft->setEnabled(true);
        ui->btnRight->setEnabled(true);
        ui->cbAuto->setEnabled(true);
        ui->cbSoundControl->setEnabled(true);
    }else {
        QString message = "ultraSound";
        SingleTon<QTcpSocket>::getInstance()->write(message.toUtf8());
        ui->btnBack->setEnabled(false);
        ui->btnForward->setEnabled(false);
        ui->btnLeft->setEnabled(false);
        ui->btnRight->setEnabled(false);
        ui->cbAuto->setEnabled(false);
        ui->cbSoundControl->setEnabled(false);
    }
}

void Widget::on_cbSoundControl_clicked()
{
    if(ui->cbSoundControl->checkState() == false){
        QString message = "normal";
        SingleTon<QTcpSocket>::getInstance()->write(message.toUtf8());
        ui->btnBack->setEnabled(true);
        ui->btnForward->setEnabled(true);
        ui->btnLeft->setEnabled(true);
        ui->btnRight->setEnabled(true);
        ui->cbAuto->setEnabled(true);
        ui->cbUltraSound->setEnabled(true);
    }else {
        QString message = "soundControl";
        SingleTon<QTcpSocket>::getInstance()->write(message.toUtf8());
        ui->btnBack->setEnabled(false);
        ui->btnForward->setEnabled(false);
        ui->btnLeft->setEnabled(false);
        ui->btnRight->setEnabled(false);
        ui->cbAuto->setEnabled(false);
        ui->cbUltraSound->setEnabled(false);
    }
}
