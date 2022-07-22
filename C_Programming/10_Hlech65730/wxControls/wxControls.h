/***************************************************************
 * Name:      wxContols.h
 * Purpose:   Defines Application Class
 * Author:    Holger Lech ()
 * Created:   2022-07-22
 * Copyright: Holger Lech ()
 * License:
 **************************************************************/

#ifndef WXCONTROLS_H
#define WXCONTROLS_H

#include <wx/app.h>

class wxControl : public wxApp
{
    public:
        virtual bool OnInit();
};

#endif // WXCONTROLS_H
