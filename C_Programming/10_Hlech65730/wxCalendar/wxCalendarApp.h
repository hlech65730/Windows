/***************************************************************
 * Name:      wxCalenderApp.h
 * Purpose:   Defines Application Class
 * Author:    Holger Lech ()
 * Created:   2022-06-09
 * Copyright: Holger Lech ()
 * License:
 **************************************************************/

#ifndef WXCALENDERAPP_H
#define WXCALENDERAPP_H

#include <wx/app.h>

class wxCalenderApp : public wxApp
{
    public:
        virtual bool OnInit();
};

#endif // WXCALENDERAPP_H
