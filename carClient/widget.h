#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>

namespace Ui {
class Widget;
}

class Widget : public QWidget
{
    Q_OBJECT

public:
    explicit Widget(QWidget *parent = nullptr);
    ~Widget();
    void appendMessage(const QString& message);
private slots:
    void on_btnForward_pressed();

    void on_btnForward_released();

    void on_btnBack_pressed();

    void on_btnBack_released();

    void on_btnLeft_pressed();

    void on_btnLeft_released();

    void on_btnRight_pressed();

    void on_btnRight_released();

    void on_btnAccelerate_clicked();

    void on_btnSlow_clicked();

    void on_cbAuto_clicked();

    void on_cbUltraSound_clicked();

    void on_cbSoundControl_clicked();

private:
    Ui::Widget *ui;
};

#endif // WIDGET_H
