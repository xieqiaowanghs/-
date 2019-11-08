#include "client.h"
#include "singleton.h"
#include "widget.h"
#include <QTcpSocket>
#include <QHostAddress>
#include "widget.h"

Client::Client(QObject *parent)
    : QObject(parent)
{
    QTcpSocket* socket = SingleTon<QTcpSocket>::getInstance();
    socket->connectToHost(QHostAddress("192.168.191.2"),9999);

    QObject::connect(socket,&QTcpSocket::readyRead,[=](){
        QString message = QString(socket->readAll());
        SingleTon<Widget>::getInstance()->appendMessage(message);
    });
}

Client::~Client()
{

}

void Client::show()
{
    SingleTon<Widget>::getReference().show();
}
