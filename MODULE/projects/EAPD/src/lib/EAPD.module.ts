import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { EAPDComponent } from './components/EAPD.component';
import { RouterModule, Routes } from '@angular/router';

import {MaterialModule} from './modules/material/material.module';
import {FlexLayoutModule} from '@angular/flex-layout';

import {FormsModule} from '@angular/forms';

const routes: Routes = [
    { path: '', component: EAPDComponent }
];

@NgModule({
    declarations: [EAPDComponent],
    imports: [
        CommonModule,
        RouterModule.forChild(routes),
        MaterialModule,
        FlexLayoutModule,
        FormsModule,
    ],
    exports: [EAPDComponent]
})
export class EAPDModule { }
