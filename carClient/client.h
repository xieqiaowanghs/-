#ifndef CLIENT_H
#define CLIENT_H

#include <QObject>
#include "loginwidget.h"

class Client : public QObject
{
    Q_OBJECT
public:
    explicit Client(QObject *parent = nullptr);
    ~Client();
    void show();
};

#endif // CLIENT_H
