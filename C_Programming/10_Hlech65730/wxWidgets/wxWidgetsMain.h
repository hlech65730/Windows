/***************************************************************
 * Name:      wxWidgetsMain.h
 * Purpose:   Defines Application Frame
 * Author:    Holger Lech (hlech65730@aol.com)
 * Created:   2022-05-20
 * Copyright: Holger Lech ()
 * License:
 **************************************************************/

#ifndef WXWIDGETSMAIN_H
#define WXWIDGETSMAIN_H

#ifndef WX_PRECOMP
    #include <wx/wx.h>
#endif

#include "wxWidgetsApp.h"

class wxWidgetsFrame: public wxFrame
{
    public:
        wxWidgetsFrame(wxFrame *frame, const wxString& title);
        ~wxWidgetsFrame();
    private:
        enum
        {
            idMenuQuit = 1000,
            idMenuAbout
        };
        void OnClose(wxCloseEvent& event);
        void OnQuit(wxCommandEvent& event);
        void OnAbout(wxCommandEvent& event);
        DECLARE_EVENT_TABLE()
};


#endif // WXWIDGETSMAIN_H
