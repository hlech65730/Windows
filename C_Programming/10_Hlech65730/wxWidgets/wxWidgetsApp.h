/***************************************************************
 * Name:      wxWidgetsApp.h
 * Purpose:   Defines Application Class
 * Author:    Holger Lech ()
 * Created:   2022-05-17
 * Copyright: Holger Lech ()
 * License:
 **************************************************************/

#ifndef WXWIDGETSAPP_H
#define WXWIDGETSAPP_H

#include <wx/app.h>

class wxWidgetsApp : public wxApp
{
    public:
        virtual bool OnInit();
};

#endif // WXWIDGETSAPP_H
