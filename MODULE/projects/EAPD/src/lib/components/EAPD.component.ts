import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';

@Component({
    selector: 'lib-EAPD',
    templateUrl: './EAPD.component.html',
    styleUrls: ['./EAPD.component.css']
})
export class EAPDComponent implements OnInit {
    constructor(private API: ApiService) { }

    ngOnInit() {
    }
}
